


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--d", type=str, required=True)
  parser.add_argument("--category", type=str, required=True)
  args = parser.parse_args()
