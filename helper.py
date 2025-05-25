import random
import numpy as np

class sol:
    def __init__(
            self,
            number_of_users: int = 1000, 
            number_of_total_files : int = 1000, 
            size_of_user_file_library: int = 50
                 ):
        """
        Args:
            number_of_users (int): Total number of users in the system.
            number_of_total_files (int): Total number of files in the system.
            size_of_user_file_libray (int):  Number of files each user is willing to seed.
        """
        self.number_of_users = number_of_users
        self.number_of_total_files = number_of_total_files
        self.size_of_user_file_library = size_of_user_file_library

        # We will say each user has 50 files that they can share if they want to.
        # this will stay constant throughout our experiment
        self.files_available_to_seed = []
        for user in range(self.number_of_users):
            self.files_available_to_seed.append(random.sample(list(range(self.number_of_total_files)), self.size_of_user_file_library))
        
        # demand is a list of lists, 1000 lists, each contains 5 files
        # represents each user's demand for five files
        demand = []
        for i in range(self.number_of_users):
            demand.append(random.sample(list(range(self.number_of_total_files)), 10))

        # Find the demand and supply for file.
        self.demand_per_file = [0] * self.number_of_total_files
        for li in demand:
            for i in li:
                self.demand_per_file[i] += 1

        # files to seed
        # List of lists. 1000 lists, each 10 files long. index represents a user. Represents the files each user is willing to share in the network.
        # IMPORTANT, this will change in future time steps. Now, we just select 4 files from each user's library of 50 files.
        self.seeders = []
        for i in range(self.number_of_users):
            self.seeders.append(random.sample(self.files_available_to_seed[i], 10))

        return


    def generate_random_preferences(
            self
            ) -> list[float]:
        
        """
        This method generates a list of ratios. The length of the list is equal to the total number of 
        files in the file sharing system. The index of the list represents the file. 
        The entry at that index represents the number of people who wish to download the file (leechers) 
        divided by the number of users who are willing to seed the file. 
        

        Returns:
            list[float]: Ratio of leechers/seeders for each file. The length of the list is equal to the total 
            number of files in the file sharing system. The index of the list represents the file. 
            The entry at that index represents the number of people who wish to download the file 
            (leechers) divided by the number of users who are willing to seed the file. 

            list[list[int]]: list of files each user is willing to seed. Randomly generate a list of files that each user already has on their file system,
            and if they are willing, could share with the network. They won't share all 50, because there is a cost to sharing (bandwidth, copyright infringement,
            ect... )

            The index of the list represents the user (ie the list at index 8 represents the 50 files that user 8 could share with the network if they wanted).
            
        """


        seeders_per_file = [0] * self.number_of_total_files
        for li in self.seeders:
            for i in li:
                seeders_per_file[i] += 1
        
        # We will use the ratio of the number of users who want the file and the number of users who are willing to provide the file 
        # to measure the ease with which a user can download a file.

        ratio_per_file = [0] * self.number_of_total_files
        for i in range(self.number_of_total_files):
            if seeders_per_file[i] == 0:
                ratio_per_file[i] = None
            else:
                ratio_per_file[i] = self.demand_per_file[i]/seeders_per_file[i]

        # if there are no seeders, it means nobody is willing to seed this file. We want to HEAVILY
        # punish this behavior, because a file that is unavailable is much worse than even a file
        # that has a very bad ratio. A file that takes an hour to download isn't as bad as file that
        # can not be downloaded at all

        # we will take the max share ratio and double it for all files that don't have any seeders.
        max_ratio = max(x for x in ratio_per_file if x != None)
        for i in range(self.number_of_total_files):
            if ratio_per_file[i] == None:
                ratio_per_file[i] = 2 * max_ratio

        
        return ratio_per_file 
    
    def calculate_latency(
            self,
            ratio_per_file: list[int]
    ) -> int:
        """
        This method will return a single number that represents the latency of the system.

        Currently it takes the square root of the mean of the squares of the demand ratio of each file. 

        The reason we choose this metric is because we want to disproportionally punish systems that have files with 
        very high demand with very little supply. A system with a modest ratios with little varitation such as: 1.2 1.3 1.9 .7, .6,
        we would expect everyone to be able to download whichever file they wanted with only a modest wait time. However, a system 
        with large variation, .6, .4, .8, 4, .5, would have some files that would be almost inaccessible or require over an hour for download.
        
        As designers for a private torrent, we consider the first system to be preferable. 

        Args:
            ratio_per_file (list[int]): Ratio of leechers/seeders for each file.
        
        Returns:
            int: latency score, square root of the mean of squares
        """
        # We are going to measure latency as the average of the squared ratios. This significantly punishes high values
        # ie files with lots of demand but very few seeders. 
        rms_latency = np.sqrt(np.mean([r**2 for r in ratio_per_file]))
        return rms_latency
    
    def recalculate(
            self,
            file_ratios: list[list[int]]
        ):
        list_of_tuples = [(file, ratio) for file, ratio in enumerate(file_ratios)]
        
        # recalculate the "supply", list of files each user is willing to generate
        # List of lists. 1000 lists, each 4 files long. Represents the files each user is 
        # willing to share in the network.
        # 
        # We take the top 4 files that have the highest score. If there is a tie, select it randomly

    
        # iterate through each user
        for user in range(self.number_of_users):
            # we randomly shuffle (we need to do this so that there users are randomly picking among ties)
            random.shuffle(list_of_tuples)
            list_of_tuples = sorted(list_of_tuples, key = lambda x: x[1], reverse=True)
        
            # this is list of files in order of worst ratio, this is the priority we will 
            # expect users to upload to maximize their ratio
            ordered_list_of_files = [index for index, ratio in enumerate(list_of_tuples)]
            self.files_available_to_seed[user] = sorted(self.files_available_to_seed[user], 
                                                        key=lambda file: ordered_list_of_files[file])

            # we will only change one file!
            if self.files_available_to_seed[user][0] in self.seeders[user]:
                pass
            else:
                self.seeders[user] = [self.files_available_to_seed[user][0]] + [self.seeders[1:]]


        seeders_per_file = [0] * self.number_of_total_files
        for li in self.seeders:
            for i in li:
                if type(i) != int:
                    print(i)
                seeders_per_file[i] += 1

        # We will use the ratio of the number of users who want the file and the number of users who are willing to provide the file 
        # to measure the ease with which a user can download a file.

        ratio_per_file = [0] * self.number_of_total_files
        for i in range(self.number_of_total_files):
            if seeders_per_file[i] == 0:
                ratio_per_file[i] = None
            else:
                ratio_per_file[i] = self.demand_per_file[i]/seeders_per_file[i]

        # if there are no seeders, it means nobody is willing to seed this file. We want to HEAVILY
        # punish this behavior, because a file that is unavailable is much worse than even a file
        # that has a very bad ratio. A file that takes an hour to download isn't as bad as file that
        # can not be downloaded at all

        # we will take the max share ratio and double it for all files that don't have any seeders.
        max_ratio = max(x for x in ratio_per_file if x != None)
        for i in range(self.number_of_total_files):
            if ratio_per_file[i] == None:
                ratio_per_file[i] = 2 * max_ratio

        
        return ratio_per_file
    
    def build_graphs(self):
        pass
        