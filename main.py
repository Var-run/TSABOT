import os
import telebot
import json
from difflib import SequenceMatcher


class Hint_obj:

  def __init__(self, x, y, ques, ans, next_clue):
    self.x = x
    self.y = y
    self.ques = ques
    self.ans = ans
    self.next_clue = next_clue
    pass


hints = [
  Hint_obj(22.319678757919636, 87.309898697082,
           "Give the older date on the plaque (same format as on plaque).",
           "3rd Day of March,1952",
           "The (now) antique which was once used as the primary in the 50s."),
  Hint_obj(
    22.31941253294504, 87.31544296829145,
    "When was it opened (same format as on plaque)?", "August 3, 1990",
    "Here they make, parathas of the faith, ask around to find out, the ones who frequently go on night outs"
  ),
  Hint_obj(22.319995810973868, 87.30309159208998,
           "How much does a Tandoori Chicken Cheese Paratha cost? (number)",
           "70", "KGP’s box office"),
  Hint_obj(
    22.31876364267983, 87.30994524097098,
    "How many buckets are in front of the TFS Office? (number)", "5",
    "Accessible only to the fastest to run around in circles, with nowhere to go"
  ),
  Hint_obj(22.318138926530693, 87.30422340759905,
           "How many lanes on the main track? (number)", "10",
           "खुले घर का घर। (khule ghar ka ghar)"),
  Hint_obj(22.318924099008626, 87.30885061045528,
           "How many entrances are there?", "6",
           "Take a dip after the annual beating"),
  Hint_obj(
    22.318090021284984, 87.30155617976125, "How many gazebo's near the lake?",
    "2",
    "A pile of pages, distraction in traces, take a quick look, in the place of the what?"
  ),
  Hint_obj(
    22.319889805335393, 87.30995699853909,
    "What is the name of the software that helps you find books in the library, look around to find out? (one word)",
    "OPAC",
    "Which is the most “Not Rational” classroom in Kharagpur and coincidentally not circular"
  ),
  Hint_obj(
    22.316463334967274, 87.3171613299342,
    "Which digit in a Nalanda room number is indicative of the block (enter position in words)",
    "second", "Mamma mia makers __mirrored__! Gimme gimme gimme the answer"),
  Hint_obj(
    22.31731881606395, 87.30767623546143,
    "How many colours does the Adda sign have? (number)", "2",
    "He stands there in plain sight, known to cure everyones plight, find where he stands with a stone chin, once you do this is the end. Fin."
  ),
  Hint_obj(
    22.319608658640686, 87.3095297928801, "What is the quote you see in red?",
    "Dedicated to the service of the nation",
    "Congratulations! You have won the hunt, send a screenshot of this message to The Scholars' Avenue on Facebook and we will get in touch with you. Look out for our selections on Facebook, prizes would be given out then"
  )
]

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start"])
def greet(message):
  with open('users.txt') as f:
    data = f.read()
  f.close()
  d = json.loads(data)
  if str(message.chat.id) not in d:
    d[str(message.chat.id)] = 0
  #print(d)
  with open('users.txt', 'w') as convert_file:
    convert_file.write(json.dumps(d))
  convert_file.close()
  bot.send_message(message.chat.id, "Hey there!")
  bot.send_message(
    message.chat.id,
    "Welcome to TSA's treasure hunt with CASH PRIZES for the top 5!")
  bot.send_message(
    message.chat.id,
    "Here you go! The first clue. \"The perfect building to start the treasure hunt, has fewer photos of its back than the front.\" For subsequent clues, keep track of your chat history and/or enter the last correct answer to your clue. \nTo enter your answer, use the /location command."
  )
  bot.send_message(
    message.chat.id,
    "Once you do enter the right coordinates and are accurate to a certain level, you would be a given a second question related to the place to ensure that you're physically at the location :) Once that answer is right, you'll be given the clues to the next place instantly."
  )
  bot.send_message(
    message.chat.id,
    "We'll try our best to ensure you have a smooth experience but if in any case you do run into errors or find the bot to be offline, know that we're aware of the situation and will try our best to fix it. If you still seem to be facing the issue then message us on The Scholars' Avenue's Facebook page! https://www.facebook.com/scholarsavenue"
  )
  with open('users.txt') as f:
    data = f.read()
  f.close()
  d = json.loads(data)
  if (d[str(message.chat.id)] > 0):
    bot.send_message(
      message.chat.id,
      f"The last correctly answered clue was clue number {d[str(message.chat.id)]} and your current clue is \"{hints[d[str(message.chat.id)]-1].next_clue}\""
    )

  with open('numbers.txt') as f1:
    numbers = f1.read()
  n = json.loads(numbers)
  if message.chat.id not in n:
    n[str(message.chat.id)] = message.from_user.first_name
  #print(n)
  with open('numbers.txt', 'w') as nconvert_file:
    nconvert_file.write(json.dumps(n))


@bot.message_handler(commands=['location'])
def regata(message):
  msg = bot.send_message(
    message.chat.id,
    'Enter latitude and longitude of the location you think the answer is using Google Maps by selecting the location and using the coordinates truncated to 5 decimal places. For example, \"56.87900 67.89534\" is a valid input. Note: Select the coordinates closest to the physical entrance to the location you think the answer might be.\n\nSeparate the latitude and longitude with a space and send your coordinates (DO NOT USE COMMAS TO INPUT LAT AND LONG): '
  )
  bot.register_next_step_handler(msg, bla)


def bla(message):
  try:
    print(
      str(message.chat.id) + " " + message.chat.first_name + " " +
      message.text)
    k = open("attempts.txt", "a")
    k.write(
      str(message.chat.id) + " " + message.chat.first_name + " " +
      message.text + "\n")
    k.close()
    data_from_tg = message.text.split()
    #load data
    lat_try = float(data_from_tg[0])
    long_try = float(data_from_tg[1])
    with open('users.txt') as f:
      data = f.read()
    d = json.loads(data)
    count = d[str(message.chat.id)]
    #check hint
    if abs(hints[count].x - lat_try) < 0.001 and abs(hints[count].y -
                                                     long_try) < 0.001:
      reply = bot.send_message(message.chat.id,
                               f"Correct, {hints[count].ques}")

      def bla2(reply):
        k = open("attempts.txt", "a")
        k.write(
          str(message.chat.id) + " " + message.chat.first_name + " " +
          reply.text + "\n")
        k.close()
        print(
          str(message.chat.id) + " " + message.chat.first_name + " " +
          reply.text)
        similarity = SequenceMatcher(None, reply.text.lower(),
                                     hints[count].ans.lower()).ratio()
        if (similarity > 0.9):
          bot.send_message(message.chat.id,
                           "Correct! Here you go, your next clue.")
          bot.send_message(message.chat.id, hints[count].next_clue)
          # with open('users.txt') as f:
          #   data = f.read()
          # f.close()
          # d = json.loads(data)
          d[str(message.chat.id)] = d[str(message.chat.id)] + 1
          with open('users.txt', 'w') as convert_file:
            convert_file.write(json.dumps(d))
          convert_file.close()
        else:
          bot.send_message(message.chat.id,
                           "Incorrect, try again with /location command.")

      bot.register_next_step_handler(reply, bla2)
    else:
      reply = bot.send_message(message.chat.id,
                               "Incorrect, try again with /location command.")

  except Exception as e:
    print(e)
    f = open("log.txt", "a")
    f.write("\n")
    f.write(
      str(message.chat.id) + " " + message.chat.first_name + " \"" +
      message.text + "\" ")
    f.write(str(e))
    f.close()
    bot.send_message(
      message.chat.id,
      "NOT A VALID INPUT, read the rules and try again with /location command."
    )


bot.polling()
