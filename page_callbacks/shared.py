import os

dream_image_key = "dream_image"
dalle_drawing_style_code = [
  "Barbizon School",
  "Cartoon",
  "Contemporary Realism",
  "Post-impressionism",
  "Plein Air Painting",
  "Scandinavian Minimalism",
  "Watercolor"
]

resources_path = f"{os.getcwd()}/resources/"
prompt_path = f"{resources_path}/prompts/"

image_generation_parameter = {
  "ratio" : "16:9",
  "size" : "1024x1024"
}
images_list_key = "images_list"