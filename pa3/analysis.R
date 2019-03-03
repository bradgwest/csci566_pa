# Analysis for PA 3

library(tidyverse)

LOG_PREFIX <- "Level 11:root:"

LOG_DIR <- "./pa3/log"
options(digits=20)

combine_logs <- function(directory, type="server") {
  fs <- list.files(directory, full.names = TRUE)
  lines <- c()
  for (f in fs) {
    if (endsWith(f, ".log") & (length(grep(type, f)) > 0)) {
      flines <- read_lines(f)
      lines <- c(lines, flines)
    }
  }
  lines
}

clean_logfile <- function(raw, separate_into = c("thread", "action", "time", "message_id", "size", "rate")) {
  tibble(raw = raw) %>% 
    filter(startsWith(raw, LOG_PREFIX)) %>% 
    mutate(raw = substring(raw, nchar(LOG_PREFIX)+1)) %>% 
    separate(raw, into = separate_into, ",")
}

send_or_rec_df <- function(df, key) {
  df %>% 
    filter(action == key)
}

join_send_and_receive <- function(df) {
  sdf <- send_or_rec_df(df, "send")
  rdf <- send_or_rec_df(df, "receive")
  sdf <- sdf %>% 
    select(sent_time = time, message_id, size, rate)
  rdf <- rdf %>% 
    select(thread, message_id, rec_time = time)
  sdf %>% 
    left_join(rdf, by = "message_id")
}

calculate_miliseconds <- function(df) {
  df %>% 
    mutate(rec_time = as.numeric(rec_time),
           send_time = as.numeric(sent_time),
           time = (rec_time - send_time)*1000)
}

stats_for_metric <- function(df) {
  df %>% 
    mutate(metric = as.numeric(metric)) %>% 
    group_by(metric) %>% 
    summarise(min_time = min(time, na.rm = T),
              mean_time = mean(time, na.rm = T),
              max_time = max(time, na.rm = T))
}

client_to_client <- function(client, metric = "size") {
  df <- client %>% 
    join_send_and_receive() %>% 
    calculate_miliseconds() %>% 
    select(metric = size, thread, time, message_id) %>% 
    stats_for_metric()
}

client_to_server <- function(client, server, metric = "size") {
  client_clean <- client %>% 
    filter(action == "send") %>% 
    select(sent_time = time, message_id, metric = size)
  server_clean <- server %>% 
    select(rec_time = time, message_id)
  client_clean %>% 
    left_join(server_clean, by = "message_id") %>% 
    calculate_miliseconds() %>%
    stats_for_metric()
}

# c("thread", "action", "time", "message_id", "size", "rate")
parse_q5_logs <- function(type="server", 
                          separate_into=c("thread", "action", "time", "message_id")) {
  vals <- c("0.0", "0.2", "0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0")
  logs = list()
  for (i in 1:length(vals)) {
    fname <- paste0(LOG_DIR, "/q5/q5_", type, "_", vals[i], ".log")
    lines <- read_lines(fname)
    df <- clean_logfile(lines, separate_into)
    df <- df %>% 
      mutate(size = as.numeric(vals[i]))
    logs[[i]] <- df
  }
  do.call(rbind, logs)
}

q3 <- function() {
  path <- paste0(LOG_DIR, "/q3")
  server_logs <- clean_logfile(combine_logs(path, type = "server"))
  client_logs <- clean_logfile(combine_logs(path, type = "client"))
  csc <- client_to_client(client_logs)
  cs <- client_to_server(client_logs, server_logs)
  View(csc)
  View(cs)
}

q5 <- function() {
  client_logs <- parse_q5_logs("client", c("thread", "action", "time", "message_id", "size", "rate"))
  server_logs <- parse_q5_logs()
  csc <- client_to_client(client_logs)
  cs <- client_to_server(client_logs, server_logs)
  View(csc)
  View(cs)
}


q7 <- function() {
  client_logs <- parse_q5_logs("client", c("thread", "action", "time", "message_id", "size", "rate"))
  server_logs <- parse_q5_logs()
  sent <- client_logs %>% filter(action == "send") %>% pull(message_id)
  rec_server <- server_logs %>% pull(message_id)
  rec_client <- client_logs %>% filter(action == "receive") %>%  pull(message_id)
  # return true if there were missing messages, otherwise false
  if (length(setdiff(sent, rec_client)) > 0 || length(setdiff(sent, rec_server)) > 0) {
    return(T)
  }
  FALSE
}
