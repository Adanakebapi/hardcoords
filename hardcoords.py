from PIL import Image

class Table:
    def __init__(self,dimensions=(1024,1024)):
        self.objects = []
        self.dimensions = dimensions
    def reset(self):
        self.objects = []
    def insert(self,obj):
        self.objects = self.objects + [obj]
    def ring(self,center=(0,0),btw=(0,500),gob=(1,1)):
        self.objects = self.objects + [self.main_ring(center,btw,gob)]
    def line(self,pos1=(-512,-512),pos2=(512,512),weight=20):
        self.objects = self.objects + [self.main_line(pos1,pos2,weight)]
    def main_ring(self,center=(0,0),btw=(0,500),gob=(1,1)):
        return (lambda x,y: btw[0] <= (((x-center[0])**2*gob[0])+((y-center[1])**2)*gob[1])**0.5 <= btw[1])
    def main_line(self,pos1=(-512,-512),pos2=(512,512),weight=20):
        centerx = (pos1[0]+pos2[0])/2
        centery = (pos1[1]+pos2[1])/2
        xs = pos1[0]-pos2[0]
        ys = pos1[1]-pos2[1]
        if (pos1[0] == pos2[0]) and (pos1[1] == pos2[1]):
            return (lambda x,y: False)
        elif (pos1[0] == pos2[0]):
            return (lambda x,y: ((pos1[0] < x < pos2[0]) or (pos2[0] < x < pos1[0])) and ((pos1[1] < y < pos2[1]) or (pos2[1] < y < pos1[1])) and (abs((x-centerx)-(y-centery)*(xs/ys)) < weight))
        else:
            return (lambda x,y: ((pos1[0] < x < pos2[0]) or (pos2[0] < x < pos1[0])) and ((pos1[1] < y < pos2[1]) or (pos2[1] < y < pos1[1])) and (abs((x-centerx)*(ys/xs)-(y-centery)) < weight)) 
    def main_function(self,x,y):
        return (True in [i(x,y) for i in self.objects])
    def get_data(self):
        data = []
        for i in range(self.dimensions[1]):
            for j in range(self.dimensions[0]):
                y = int(self.dimensions[1]/2)-i
                x = j-int(self.dimensions[0]/2)
                if self.main_function(x,y):
                    data += [(255,255,255)]
                else:
                    data += [(0,0,0)]
        return data
    def create_img(self):
        data = self.get_data()
        img = Image.new("RGB",self.dimensions)
        img.putdata(data)
        return img
    def save(self,filename):
        img = self.create_img()
        img.save(filename)
        img.close()
    def show(self):
        img = self.create_img()
        img.show()
        img.close()
