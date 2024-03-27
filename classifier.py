import base64
import shutil
import os
import pytesseract
from PIL import Image
from openai import OpenAI

# OpenAI API Key
api_key = ""
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

client = OpenAI(api_key=api_key)







def create_directory_if_not_exists(directory_path):
  # Check if the directory already exists
  if not os.path.exists(directory_path):
    # Create the directory
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
  else:
    print(f"Directory already exists: {directory_path}")

def move_file(source_file, target_directory):
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
      print(f"Target directory does not exist: {target_directory}")
      return

    # Construct the full path for the target file
    target_file = os.path.join(target_directory, os.path.basename(source_file))

    # Move the file
    try:
      shutil.move(source_file, target_file)
      print(f"File moved successfully to {target_file}")
    except Exception as e:
      print(f"Error moving file: {e}")



# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


if __name__ == '__main__':


  base_path = 'C:\\photo\\'
  categories = ["restaurant", "book", "traffic", "hotel", "other"]
  for item in categories:
    create_directory_if_not_exists(base_path + item)

  # Path to your image
  # image_name = "gggg.PNG"

  categories_text = ""
  for i, category in enumerate(categories):
    if i == len(categories) - 1:
      # For the last item, prepend 'and'
      categories_text += "and " + category
    else:
      # For other items, append the category and a comma
      categories_text += category + ", "

  print(categories_text)


  # Getting the base64 string
  # base64_image = encode_image(base_path + image_name)


  for image_name in os.listdir(base_path):
    image_path = base_path + image_name
    if os.path.isdir(image_path):
      # Skip this iteration if it's a directory
      continue
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="jpn")

  # headers = {
  #   "Content-Type": "application/json",
  #   "Authorization": f"Bearer {api_key}"
  # }
  #
  # payload = {
  #   "model": "gpt-4-vision-preview",
  #   "messages": [
  #     {
  #       "role": "user",
  #       "content": [
  #         {
  #           "type": "text",
  #           # "text": "この領収書は以下の種類から分類しなさい?飲食代、書籍代、ホテル代、交通代、その他。飲食費用、書籍費用、交通費用、宿泊費用と不明の５種類名のみを答えなさい"
  #           # "text": "まず、図にある文字を全部を認識して、それに基づいて、飲食費用、書籍費用、交通費用、宿泊費用のうち、この領収書はどれかに分類しなさい?ただし、自信がないときに、不明に分類しなさい。"
  #           "text": "Recognize the type of the receipt. restaurant, book, traffic, hotel or the other. If there is some kind of food name inside the image, categorize it as restraurant."
  # },
  #         {
  #           "type": "image_url",
  #           "image_url": {
  #             "url": f"data:image/jpeg;base64,{base64_image}"
  #           }
  #         }
  #       ]
  #     }
  #   ],
  #   "max_tokens": 300
  # }
  #
  # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)



    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "user", "content": "Based on the following japanese recognized from a receipt, judge the kind of receipt from " + categories_text + ". Only answer the type!" + text},
      ]
    )

    # print(response.choices[0].message.content)
    result = response.choices[0].message.content

    for item in categories:
      if item == result:
        move_file(image_path, base_path+result)
        break

