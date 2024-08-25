import  keras 
import  tensorflow as  tf

class  Load_Model:
    def __init__(self, model_path, img_path):
        self.model_path  = model_path
        self.img_path  = img_path
        self.label_dict = {"bacterial leaf blight":0, "brown spot":1, "leaf blast":2}
        
    def  load_mobilenet_model(self):
        self.model = keras.models.load_model(self.model_path)
        return self.model
    def  image_processor(self):
        img = keras.utils.load_img(self.img_path,  target_size=(150,150))
        img_arr_ = keras.utils.img_to_array(img)
        self.img_arr  = tf.expand_dims(img_arr_/255.0, axis=0)
        return self.img_arr
    def  predict_image_class(self):
        self.label_predicted   = self.load_mobilenet_model().predict(self.image_processor())
        self.disease   = [key for  key, value  in  self.label_dict.items() if  value  == tf.argmax(self.label_predicted, axis=1)]
        return  self.disease
    
#obj  = Load_Model(model_path="/home/wambugu/Downloads/mobilenet_model_rice_disease_classification.keras",img_path="/home/wambugu/blight.jpeg")     