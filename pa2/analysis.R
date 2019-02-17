# Analysis for programming assignment 2

library(tidyverse)

RESULTS_DIR = "./pa2/results/"

split_rows <- function(df) {
  df %>% 
    separate(raw, into=c("direction", "vals"), ": ") %>% 
    separate(vals, into=c("letter", "time", "size"), ",")
}

# QUESTION 3
client_raw <- read_lines(paste0(RESULTS_DIR, "/q3_client.csv"))
parse_client_raw <- function(client_raw) {
  client_short <- client_raw[2:(length(client_raw) - 3)]
  tibble(raw = client_short) %>% 
    filter(startsWith(raw, "mt-")) %>% 
    split_rows() %>% 
    mutate(direction=substring(direction, 4, length(direction))) %>% 
    filter(letter != "$") %>% 
    mutate(size=as.numeric(size),
           time = as.numeric(time))
}
client <- parse_client_raw(client_raw)

server_raw <- read_lines(paste0(RESULTS_DIR, "/q3_server.csv"))
parse_server_raw <- function(server_raw) {
  tibble(raw = server_raw) %>% 
    filter(startsWith(raw, "mt-")) %>% 
    split_rows() %>% 
    mutate(direction=substring(direction, 4, length(direction))) %>% 
    mutate(size_actual = 0,
           time = as.numeric(time))
}
server <- parse_server_raw(server_raw)
size = 1
i = 1
while (i < nrow(server)) {
  if (server$letter[i] != "$") {
    server$size_actual[i] <- size
  } else {
    size = size * 2
    while ((i + 1) < nrow(server) & server$letter[i+1] == "$") {
      i = i + 1
    }
  }
  i = i + 1
}

server <- server %>% mutate(size = size_actual) %>% 
  select(direction, letter, time, size) %>% 
  filter(letter != "$")

client_grouped <- client %>% 
  group_by(direction, letter, size) %>% 
  summarize(min_time = min(time), max_time = max(time))

client_send_grouped <- client_grouped %>% 
  filter(direction == "send")
client_rec_grouped <- client_grouped %>% 
  filter(direction == "rec")

server_grouped <- server %>% 
  group_by(direction, letter, size) %>% 
  summarise(min_time = min(time), max_time = max(time))

# C-S
cs <- client_send_grouped %>% 
  full_join(server_grouped, by=c("letter", "size")) %>% 
  mutate(message_time = max_time.y - min_time.x) %>% 
  group_by(size) %>% 
  summarise(mean_delay = mean(message_time, na.rm = T),
            min_delay = min(message_time, na.rm = T),
            max_delay = max(message_time, na.rm = T))

write_csv(cs, "./pa2/results/q3cs.csv")

# C-S-C
csc <- client_send_grouped %>% 
  full_join(client_rec_grouped, by=c("letter", "size")) %>% 
  mutate(message_time = max_time.y - min_time.x) %>% 
  group_by(size) %>% 
  summarise(mean_delay = mean(message_time, na.rm = T),
            min_delay = min(message_time, na.rm = T),
            max_delay = max(message_time, na.rm = T))

write_csv(csc, "./pa2/results/q3csc.csv")

# QUESTION 4
