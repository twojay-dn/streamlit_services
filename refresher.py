import streamlit as st

def display_hint_list(asset, hint_list):
  asset.write(hint_list)
  
def display_calculated_hint_list(asset, hint_dict):
  asset.write(hint_dict)

def refresh_impl(postprocessed):
  if postprocessed.is_contain("hints"):
    display_hint_list(
      postprocessed.get("generated_hint_list_display_position"),
      postprocessed.get("hints")
    )
    display_calculated_hint_list(
      postprocessed.get("calculated_hint_list_display_position"),
      postprocessed.get("calculated_hint_dict")
    )
  return postprocessed
class Refresher:
  @staticmethod
  def run(postprocessed):
    return refresh_impl(postprocessed)
