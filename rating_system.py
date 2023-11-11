import os


class RatingSystem:
    def __init__(self, save_directory):
        self.save_directory = save_directory
        # Ensure the save directory exists
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def save_rating_and_reaction(self, video_name, rating, reaction):
        # Save the rating and reaction to a file
        file_path = os.path.join(self.save_directory, f"{video_name}.txt")
        with open(file_path, 'w') as file:
            file.write(f"Rating: {rating}\nReaction: {reaction}\n")

    def get_rating_and_reaction(self, video_name):
        # Retrieve the rating and reaction from a file
        file_path = os.path.join(self.save_directory, f"{video_name}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        return None
