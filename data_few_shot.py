"""
manage saved data for the few shot algorithm
"""
import numpy as np


class DataFewShot:
    """represent the data saved for few shot learning
    attributes :
        num_classe : max number of class handled
        data_type : how to initialize unseen class (demo/cifar)
        mean_features(np.ndarray or list(np.ndarray)) : mean of the feature / list of feature to aggregate 
        registered_classes : registered class
        shot_list : list of the regitered data
    """

    def __init__(self,num_class,data_type="cifar"):
        self.data_type=data_type
        if self.data_type=="demo":
            self.shot_list=[]
        elif self.data_type=="cifar":
            self.shot_list=[[] for i in range(num_class)]
        else:
            raise NotImplementedError(f"datatype {data_type} is not implemented")
        self.num_class=num_class
        
        self.mean_features=[]
        self.registered_classes=[]
        self.is_recorded=False

    def add_repr(self,classe,repr):
        """
        add the given repr to the given classe
        """
        self.is_recorded=True
        repr=repr#.detach().cpu().numpy()

        if classe not in self.registered_classes:
            self.registered_classes.append(classe)
            if self.data_type=="demo":
                self.shot_list.append(repr)
            elif self.data_type=="cifar":
                self.shot_list[classe]=repr
            
        else:
            #TODO : change dtype to numpy array
            self.shot_list[classe] = np.concatenate(
                (self.shot_list[classe], repr), axis=0
            )
    def get_shot_list(self):
        return self.shot_list#[shot.detach().cpu().numpy() for shot in self.shot_list]

    def get_mean_features(self):
        return self.mean_features

    def is_data_recorded(self):
        return self.is_recorded
    

    def aggregate_mean_rep(self):
        """
        aggregate all saved features
        can only be called once

        """
        self.mean_features=np.concatenate(self.mean_features,axis=0)
        self.mean_features=self.mean_features.mean(axis=0)

  
        
    def add_mean_repr(self,features):
        """
        add a given image to the mean repr of the datas
        """
        
        self.mean_features.append(features)

    
    def reset(self):
        """
        reset the saved image, but not the mean repr
        """
        self.shot_list=list(range(self.num_class))
        self.registered_classes=[]