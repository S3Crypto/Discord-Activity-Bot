from datetime import datetime, timedelta, timezone


# measures the amount of idle time between now and then (the given timestamp, which should be user's last message or
# last active in voice comms.


def checkIdleTime(ts):
    current_time = datetime.utcnow()
    difference = current_time - ts
    duration_in_seconds = difference.total_seconds()
    days = timedelta(seconds = duration_in_seconds).days
    remaining_seconds = timedelta(seconds = duration_in_seconds).seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds // 60) % 60

    return days, hours, minutes



def filterChannels(channels):
    text_channels = []

    for chan in channels:
        if str(chan.type) == 'text':
            text_channels.append(chan)

    return text_channels


async def getMessages(channels):
    messages = []
    for chan in channels:
        async for message in chan.history(limit=500):
            messages.append(message)

    return messages

def getLastMessage(msg_arr, user):
    user_messages = []

    for msg in msg_arr:
        if msg.author == user:
            user_messages.append(msg)

    return user_messages[0] if user_messages else None

def calculateUserMessagePercentage(messages, user):
    total_messages = len(messages)
    user_messages_count = 0

    for msg in messages:
        if msg.author == user:
            user_messages_count += 1

    if total_messages == 0:
        return 0

    user_message_percentage = (user_messages_count / total_messages) * 100
    return user_message_percentage




def generateIdleMessage(time_idle):
    msg_str = ''

    if len(time_idle) == 6:
        msg_str = f' has been idle for {time_idle[0]} years, {time_idle[1]} months, {time_idle[2]} weeks, ' \
                  f'{time_idle[3]} days, {time_idle[4]} hours, and {time_idle[5]} minutes.'
    elif len(time_idle) == 5:
        msg_str = f' has been idle for {time_idle[0]} months, {time_idle[1]} weeks, ' \
                  f'{time_idle[2]} days, {time_idle[3]} hours, and {time_idle[4]} minutes.'
    elif len(time_idle) == 4:
        msg_str = f' has been idle for {time_idle[0]} weeks, {time_idle[1]} days, {time_idle[2]} hours, and ' \
                  f'{time_idle[3]} minutes.'
    elif len(time_idle) == 3:
        if time_idle[0] == -1:
            msg_str = ' is currently active.'
        else:
            msg_str = f' has been idle for {time_idle[0]} days, {time_idle[1]} hours, and {time_idle[2]} minutes.'

    return msg_str