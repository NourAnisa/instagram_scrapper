import random as r
import csv

class RandomPicker():
    def __init__(self, data):
        self.total_award = {}
        self.data = data
    
    def pick_winner(self, num):
        award = {}
        while len(award) < num:
            pick = r.choice(self.data)
            writer = pick["writer"]
            std_id = pick["std_id"]

            if writer not in self.total_award:
                award[writer] = std_id
        
        self.total_award.update(award)
        return award
    
    def print_winners(self, dict, filename):
        print(f"🎉 Congratulation for Getting {filename}!")
        
        for writer, std_id in dict.items():
            print(f'인스타 계정 : {writer} / 학번 : {std_id}')
        
        try:
            self.save_to_csv(dict, filename)
            print(f"✅ Successfully Saved to {filename}.csv")
        except:
            print("❗️ Failed to Saving CSV file.")
            raise Exception


    def save_to_csv(self, dict, filename):
        f = open(f'{filename}.csv', 'w', newline='')
        wr = csv.writer(f)
        for idx, (writer, std_id) in enumerate(dict.items()):
            wr.writerow([idx + 1, writer, std_id])
        f.close()