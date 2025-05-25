class sol:
    def __init__(self):
        pass

    def generate_random_preferences(
            self, 
            number_of_users: int = 1000, 
            number_of_total_files : int = 1000, 
            number_of_files_per_user_seed: int = 50
            ) -> list[float]:
        
        """
        This method generates a list of ratios. The length of the list is equal to the total number of 
        files in the file sharing system. The index of the list represents the file. 
        The entry at that index represents the number of people who wish to download the file (leechers) 
        divided by the number of users who are willing to seed the file. 

        Args:
            number_of_users (int): Total number of users in the system.
            number_of_total_files (int): Total number of files in the system.
            number_of_files_per_user_seed (int): Number of files each user is willing to seed. 

        Returns:
            list[float]: 
        """
        
        ratio_per_file = [0 for _ in range(number_of_total_files)]

        
        return ratio_per_file