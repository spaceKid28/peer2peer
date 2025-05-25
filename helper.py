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
        # demand is a list of lists, 1000 lists, each contains 5 files
        # represents each user's demand for five files
        demand = []
        for i in range(self.number_of_users):
            demand.append(random.sample(list(range(self.number_of_total_files)), 5))

        # We will say each user has 50 files that they can share if they want to.
        files_available_to_seed = []
        for user in range(self.number_of_users):
            files_available_to_seed.append(random.sample(list(range(self.number_of_total_files)), self.size_of_user_file_library))

        # files to seed
        # List of lists. 1000 lists, each 4 files long. Represents the files each user is willing to share in the network.
        # IMPORTANT, this will change in future time steps. Now, we just select 4 files from each user's library of 50 files.
        seeders = []
        for i in range(self.number_of_users):
            seeders.append(random.sample(files_available_to_seed[i], 4))

        # Find the demand and supply for file.
        demand_per_file = [0] * self.number_of_total_files
        for li in demand:
            for i in li:
                demand_per_file[i] += 1

        seeders_per_file = [0] * self.number_of_total_files
        for li in seeders:
            for i in li:
                seeders_per_file[i] += 1
        
        # We will use the ratio of the number of users who want the file and the number of users who are willing to provide the file 
        # to measure the ease with which a user can download a file.

        ratio_per_file = [0] * self.number_of_total_files
        for i in range(self.number_of_total_files):
            if seeders_per_file[i] == 0:
                # we are going to assign a very large number for files with no seeders. 
                # PROBABLY SHOULD CHANGE THIS
                ratio_per_file[i] = 20
            else:
                ratio_per_file[i] = demand_per_file[i]/seeders_per_file[i]
        
        return ratio_per_file, files_available_to_seed
    
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
    
    def recalculate(self, rms_latency):

        return rms_latency
        