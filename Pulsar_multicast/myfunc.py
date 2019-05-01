# from pulsar import Function

from pulsar import Function

# Example function that uses the built in publish function in the context
# to publish to a desired topic based on config
class RoutingFunction(Function):
  def __init__(self):
    pass

  def process(self, item, context):
    # publish_topic = "publishtopic"
    # if "publish-topic" in context.get_user_config_map():
      # publish_topic = context.get_user_config_value("publish-topic")
    context.publish( "persistent://public/default/topic1",item)
    context.publish( "persistent://public/default/topic2",item)
    # context.publish("topic2",input + '!')
    return
