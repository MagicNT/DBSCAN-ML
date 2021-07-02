# DBSCAN Algorithm

## **Implementation**

### Scripting Language

- Python 3

### Dataset

- Dataset 1 excerpt [2-D]:

```
-21.0241928445288,-12.8707393016064
22.57981297913,-2.42799507799931
-24.1021895544148,-0.289140839729988
15.7020144354096,18.1569107543476
20.7975486041035,2.60964260790946
-21.8298914827546,-6.92002167083324
3.81619228460648,-20.5464491367091
-20.109504761691,-6.36941459093681
```

- Dataset 2 excerpt [2-D or 3-D]:

```
0.85,17.45,2
0.75,15.6,2
3.3,15.45,2
5.25,14.2,2
4.9,15.65,2
5.35,15.85,2
5.1,17.9,2
4.6,18.25,2
4.05,18.75,2
3.4,19.7,2
2.9,21.15,2
3.1,21.85,2
3.9,21.85,2
4.4,20.05,2
7.2,14.5,2
7.65,16.5,2
```

### Import Libraries

- We import the csv Python library to read in the dataset saved inside a CSV file
- We import the prettytable Python library to present the output results in a nice tabular layout
- We import the scipy Python library to utilize its Euclidean distance function
- We import the matplotlib Python library to create interactive plot visualization for showcasing the resulting support vectors


```python
import csv
import prettytable
import scipy.spatial as scp
import matplotlib.pyplot as matp
```

### Plot Class

We implemented a module for handling all plotting operations whenever the algorithm has concluded and results are ready to be displayed. In the initialization function of the class we pass along as parameters the clustering dimension and we make place for the plotting colors for each different cluster as well as for the scattering axis.


```python
class Plot:

	def __init__(self, dimension):
		self.colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
		self.dimension = dimension
		self.ax = None
```

### Drawing Data Points

In the below implemented routines we pass corresponding clusters wich hold their datapoints coordinates and with these vectors we place them on the plot in preparation to display the final figure at the end. We give each cluster a corresponding marker (X, O) as well as color for its datapoints. Additioally, we distinguish noise datapoints by a seperate marker and color, by implementing a different class function for placing such points on the figure.


```python
	def draw_point(self, count, added_cluster):
		color = self.colors[count%len(self.colors)]
		if self.dimension == 2:
			self.ax.scatter(added_cluster.X(), added_cluster.Y(), c=color, marker="o", label="Cluster {}".format(added_cluster.ID))
		elif self.dimension == 3:
			self.ax.scatter(added_cluster.X(), added_cluster.Y(), added_cluster.Z(), marker="o",  c=color, label="Cluster {}".format(added_cluster.ID))


	def draw_noise(self, noise_cluster):
		if self.dimension == 2:
			self.ax.scatter(noise_cluster.X(), noise_cluster.Y(), marker = "x", label = noise_cluster.ID)
		elif self.dimension == 3:
			self.ax.scatter(noise_cluster.X(), noise_cluster.Y(), noise_cluster.Z(), marker = "x", label = noise_cluster.ID)

```

### Make Plot

The below routines create a figure object based on the specified dimensionality (2-D or 3-D) and set up the plotting area and the plot legend and title. When the plot figure has been created and the datapoints scattered over the plot, we can call over the plot function to display the visualization for the final clustering layout overview.


```python
	def setup_figure(self):
		fig = matp.figure()
		if self.dimension == 2:
			self.ax = fig.add_subplot(111, projection="rectilinear")
		elif self.dimension == 3:
			self.ax = fig.add_subplot(111, projection="%dd"%3)


	def plot(self):
		matp.title("DBSCAN", fontsize=15)
		self.ax.legend(loc="upper right")
		matp.show()
```

### Cluster Class

In order to neatly manage and organize the handled clusters throughout the algorithm runtime, we implemented a seperate class for cluster objects. These objects have as local variables, unique IDs to allow us to recognize different cluster objects and a corresponding array for holding datapoints that belong to the managed cluster object. It should be noted that we required the need for a routine that allows us to add new datapoints to the cluster, a routine to check whether a point belongs to the corresponding cluster and 3 functions to return all the X, Y and Z (if 3-D) coordinates of all the datapoints whithin the cluster object.


```python
class Cluster:

	def __init__(self, ID):
		self.ID = ID
		self.points = []

	def add_point(self, point):
		self.points.append(point)

	def not_in(self, point):
		return point not in self.points

	def X(self):
		return [coord[0] for coord in self.points]
	
	def Y(self):
		return [coord[1] for coord in self.points]

	def Z(self):
		return [coord[2] for coord in self.points]
```

### DBSCAN Algorithm Class

In this assignment question we will implement a DBSCAN algorithm for clustering 2-D and 3-D datapoints. We implemented the algorithm in a modular form as a class for better management and manipulation control. It should be noted that the local class variables represent  the name of the input file from which we will grab the dataset for processing, the radius of neighborhood (Epsilon value), the minmum number of points and the dimensionality of the datapoints (from the imported dataset) on which we will do the clustering.


```python
class Dbscan:
	
	def __init__(self, filename="data/annulus.csv", eps=2.5, min_points=2, dimension=2):
		self.filename = filename
		self.dataset = []
		self.eps = eps
		self.min_points = min_points
		self.dimension = dimension
		self.clusters = set()
		self.cluster_count = 0
		self.visited_points = []
		self.import_dataset()
```

### Importing/Pre-Processing Dataset

In the below routine we import the corresponding dataset file and directly convert the read strings into numeric values


```python
	def import_dataset(self):
		with open(self.filename, "rt") as dataset_csvfile:
			dataset_reader = csv.reader(dataset_csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
			self.dataset = list(dataset_reader)
```

### Region Query Routine

Thenbelow implemented routine is utilized by the algorithm by providing it as a paramater a specified point (which is an arrary holding the point's 2-D or 3-D coordinates). With this point at hand, we prompt every point within our dataset (except the point itself which already is taken from the same dataset) and with that we calculate the Euclidean distance from our input point to every other point in the dataset. If this calculated resulting distance is <= eps, then we append this compared point from the dataset iteration to a resulting array and so on for other points. Eventually we return this array to the caller function.


```python
	def region_query(self, s_point):
		r = []
		for d_point in self.dataset:
			if s_point != d_point:
				if scp.distance.euclidean(d_point[:self.dimension], s_point[:self.dimension]) <= self.eps:
					r.append(d_point)
		return r
```

### Display Results

In the below routine, we print the final results, the number of total clusters found. We do this by presenting to the view a nice tabular form in which each point with its 2-D or 3-D coordinates are shown along with the corresponding cluster ID that each point belongs to. In addition, we also give the points that are clustered as Noise or outliers.


```python
	def display(self):
		print (" [+] Total Number of Clusters: {} \n".format(self.cluster_count))
		if self.dimension == 2:
			t = prettytable.PrettyTable(["Cluster ID", "X Coordinate", "Y Coordinate"])
		elif self.dimension == 3:	
			t = prettytable.PrettyTable(["Cluster ID", "X Coordinate", "Y Coordinate", "Z Coordinate"])
		for cluster in self.clusters:
			for point in cluster.points:
				if self.dimension == 2:
					t.add_row([cluster.ID, point[0], point[1]])
				elif self.dimension == 3:
					t.add_row([cluster.ID, point[0], point[1], point[2]])
		print(t)
```

### Expand Cluster

A point is selected which has at least minPts within its epsilon radius. Then each point that is within the neighborhood of the core point is evaluated to determine if it has the minPts nearby within the epsilon distance. If the point does meet the minPts criteria it becomes another core point and the cluster expands. If a point does not meet the minPts criteria it becomes a border point. The cluster is complete as it becomes surrounded by border points because there are no more points within the epsilon distance. A new random point is selected and the process repeats to identify the next cluster.


```python
	def expand_cluster(self, cluster, point, neighbour_points):
		cluster.add_point(point)
		for p in neighbour_points:
			if p not in self.visited_points:
				self.visited_points.append(p)
				np = self.region_query(p)
				
				if len(np) >= self.min_points:
					for n in np:
						if n not in neighbour_points:
							neighbour_points.append(n)
					
				for other_cluster in self.clusters:
					if other_cluster.not_in(p):
						if cluster.not_in(p):
							cluster.add_point(p)

				if self.cluster_count == 0:
					if cluster.not_in(p):
						cluster.add_point(p)
						
		self.clusters.add(cluster)
```

### Initiate Algorithm

In the starting routine, we make a Plot object and setup the final figure canvas on which we will add points as we go. Then, we create a noise cluster object to add outliers into it. Next, we loop over every point in the dataset, and if this point is not visited before we add it to the visited array then proceed to check its region for neighbouring points using Euclidean distance. If the length of the resulting returned neighbouring points array is less than the specified minimum points value determined at the beignning of the program, we add this point to the noise clutser. And if not so, we create a new cluster and increment the total counting number of these clusters, then we expand this specified cluster using the implemented expand_cluster routine. Afterwards, we pass this cluster objects (along with its in-array of belonging points) to the Plot object we previously created so that we can add its points to the final plot figure. Eventually, when we are done looping over every point in the dataset, we move along to the noise cluster to add its points to the plot figure since these outiers also have to be plotted. At the conlusion, we display cluster table results and pop the final plot visualization to show these clusters.


```python
	def start(self):
		P = Plot(self.dimension)
		P.setup_figure()
		
		noise_cluster = Cluster("Noise")
		self.clusters.add(noise_cluster)

		for point in self.dataset:
			if point not in self.visited_points:
				self.visited_points.append(point)
				neighbour_points = self.region_query(point)
				
				if len(neighbour_points) < self.min_points:
					noise_cluster.add_point(point)
				else:
					ID = self.cluster_count
					added_cluster = Cluster(ID)
					self.cluster_count += 1
					self.expand_cluster(added_cluster, point, neighbour_points)
					P.draw_point(self.cluster_count, added_cluster)
		
		if noise_cluster.points != []:
			P.draw_noise(noise_cluster)
		self.display()
		P.plot()
```

### Driver Routine

Below is the main driver routine which creates 3 Dbscan objects a a time and runs the algorithm for each of them to show diverse results and plots. For the first 2-D dataset we explicitly set the dimensionality to 2 then run its procedure on it. As for the second dataset which contains 2-D and 3-D coordinates, we show two runtimes for each dimension where at first we run for dimension 2 then for dimension 3, and in each runtime we display the table clustering results followed up by a final plot showing the clustering.


```python
def main():
	print("\n" + "="*70)
	print(" DBSCAN Algorithm")
	print("="*70 + "\n")
	Dbscan(filename="annulus.csv", dimension=2).start()
	Dbscan(filename="jain.csv", dimension=2).start()
	Dbscan(filename="jain.csv", dimension=3).start()
```

### Output

    
    ======================================================================
     DBSCAN Algorithm
    ======================================================================
    
     [+] Total Number of Clusters: 2 
    
    +------------+---------------------+---------------------+
    | Cluster ID |     X Coordinate    |     Y Coordinate    |
    +------------+---------------------+---------------------+
    |     0      |  -21.0241928445288  |  -12.8707393016064  |
    |     0      |  -21.5539677518206  |  -10.7266022757285  |
    |     0      |  -19.6262632238801  |  -11.8537678089243  |
    |     0      |  -20.2664023010369  |  -13.1471838281244  |
    |     0      |  -22.0587669159559  |   -11.68545325598   |
    |     0      |  -20.5308454090407  |  -13.8364284945822  |
    |     0      |   -21.797729980572  |  -10.6270568145565  |
    |     0      |  -20.1397832460421  |  -14.5827768554831  |
    |     0      |  -19.7661830786458  |  -13.5366521722342  |
    |     0      |  -19.9706482677584  |  -13.2708592518563  |
    |     0      |  -21.3065227942106  |  -12.8517751292567  |
    |     0      |  -21.4038262359816  |  -11.2096912163355  |
    |     0      |  -19.6332746393202  |   -11.616101598654  |
    |     0      |  -19.8386372741492  |  -12.0804675561751  |
    |     0      |  -20.4161440932267  |  -9.74003602040002  |
    |     0      |  -21.1085246857761  |  -9.20374574335466  |
    |     0      |  -21.0226279432059  |  -10.0953008910154  |
    |     0      |  -21.2816105206877  |  -9.52119053551983  |
    |     0      |  -21.9741967725447  |  -8.37321217794587  |
    |     0      |  -20.3323137226199  |  -9.26053839934084  |
    |     0      |  -20.9825978595682  |   -9.0486586252454  |
    |     0      |  -18.4939391880734  |  -13.7149716442055  |
    |     0      |  -17.2412193344167  |  -11.7566265569798  |
    |     0      |  -17.5221668754342  |  -11.0503890253838  |
    |     0      |  -17.7350836073677  |   -10.344316128336  |
    |     0      |  -18.4183225005019  |  -9.90246584867242  |
    |     0      |  -18.3383601220969  |  -12.8449738900387  |
    |     0      |  -18.4786839845957  |   -12.339171714773  |
    |     0      |  -18.2265410633881  |  -13.8388708647522  |
    |     0      |  -19.3770519897235  |  -14.8786139860184  |
    |     0      |  -18.6496811656513  |  -15.2466092911766  |
    |     0      |  -23.3243029556816  |  -8.93080932271239  |
    |     0      |  -18.3396579666714  |  -16.1202716832609  |
    |     0      |  -18.3133718293688  |  -15.8289947504313  |
    |     0      |  -20.5275363267993  |   -7.3971605312066  |
    |     0      |  -18.8690967596458  |  -7.84646579196978  |
    |     0      |  -21.1545456881423  |  -7.85788282885117  |
    |     0      |  -21.8298914827546  |  -6.92002167083324  |
    |     0      |  -21.7929076621276  |  -7.52535720007743  |
    |     0      |  -22.0036116647551  |  -7.50081764184908  |
    |     0      |  -23.1085881116374  |  -6.17642310968434  |
    |     0      |  -22.5887604279391  |  -6.14598625392932  |
    |     0      |  -23.8669599168314  |  -7.11124231205845  |
    |     0      |  -23.2992849304803  |  -7.33234411214122  |
    |     0      |  -21.5815234680574  |  -6.56147491259569  |
    |     0      |  -16.4902846522118  |  -12.6137588581134  |
    |     0      |  -16.0495366160989  |   -14.134213416434  |
    |     0      |  -16.7670777727696  |   -13.465373445519  |
    |     0      |  -16.7409814157248  |  -12.9521244382263  |
    |     0      |  -17.1865839474772  |  -14.0721058887765  |
    |     0      |  -16.4827226621484  |  -12.6106966927697  |
    |     0      |   -16.631155503742  |  -12.4323523312026  |
    |     0      |   -17.036789186316  |  -11.4215233067151  |
    |     0      |  -15.9588591619203  |  -12.9284217664639  |
    |     0      |  -15.9033628836755  |  -12.3864748689283  |
    |     0      |   -15.560867493302  |  -13.3901459110855  |
    |     0      |  -15.8693610415186  |  -12.2918670472185  |
    |     0      |  -16.5337257979129  |  -11.4405973052795  |
    |     0      |  -16.5110365913767  |  -16.8727228147316  |
    |     0      |   -20.109504761691  |  -6.36941459093681  |
    |     0      |  -21.1156428075003  |  -5.82512110975809  |
    |     0      |  -20.6233851358403  |  -5.64330400929009  |
    |     0      |  -18.8100357976789  |  -7.19063630429592  |
    |     0      |  -19.2865953754106  |   -5.5993638609533  |
    |     0      |  -22.4925203935674  |   -5.7265315580771  |
    |     0      |  -24.4576231108315  |  -4.16810057552908  |
    |     0      |  -23.6254817101292  |  -4.96022488454367  |
    |     0      |  -23.6413166153437  |  -4.29834594451745  |
    |     0      |  -15.2017359110535  |  -13.7783069344136  |
    |     0      |  -15.2916668170559  |  -16.0252736141092  |
    |     0      |  -15.5559047779794  |  -15.2514549392515  |
    |     0      |  -15.1332378807167  |   -15.648845951375  |
    |     0      |  -15.3088743054815  |  -15.0059289019582  |
    |     0      |  -14.5650688277395  |  -15.0532415788869  |
    |     0      |  -14.0321269114651  |  -17.0562086357066  |
    |     0      |  -14.2136666640703  |  -17.0498306825989  |
    |     0      |   -16.101948679938  |  -18.9060113364393  |
    |     0      |  -14.9393158219472  |  -17.2379155607139  |
    |     0      |  -14.4846420453324  |  -16.6912695587106  |
    |     0      |  -14.4628873045849  |  -17.7742375027268  |
    |     0      |  -14.7681595709958  |  -17.6882502588854  |
    |     0      |  -19.8590935183964  |  -4.63565482275358  |
    |     0      |  -20.8082586507351  |  -3.59013878209057  |
    |     0      |  -23.9061922528344  |  -3.51558196289259  |
    |     0      |   -23.73660891258   |  -2.46933781424041  |
    |     0      |  -23.8606518129169  |  -2.72626200584986  |
    |     0      |  -23.9639922506008  |  -2.41100493697962  |
    |     0      |  -24.1222194624703  |  -2.02785550012619  |
    |     0      |  -24.0472272965346  |  -2.93793807641507  |
    |     0      |  -23.2081004177258  |  -2.98272167704195  |
    |     0      |  -22.5491926528277  |   -3.0952415792715  |
    |     0      |  -21.8530608326444  |  -3.27282055666336  |
    |     0      |  -21.5524921643326  |  -3.24704173405051  |
    |     0      |  -13.4110399933583  |  -15.2636669065168  |
    |     0      |  -13.9774272399849  |  -15.8663319381263  |
    |     0      |  -13.7310724187321  |  -16.0669726510844  |
    |     0      |  -13.4791044930364  |  -16.4373414085421  |
    |     0      |  -12.8333249072699  |  -16.6515073467286  |
    |     0      |  -13.7674481788499  |  -18.5081387839784  |
    |     0      |  -13.1546661202585  |   -18.623524971131  |
    |     0      |  -12.7073522599914  |  -18.9155728527883  |
    |     0      |   -14.874355513544  |  -18.9859125269511  |
    |     0      |  -14.9390902556195  |  -19.9093941109764  |
    |     0      |  -14.7218367502661  |  -20.0039775786009  |
    |     0      |  -20.9545765518931  |  -2.47678110724165  |
    |     0      |  -20.1706069266287  |  -2.89369718073574  |
    |     0      |  -19.9296870478101  |  -2.82181896167892  |
    |     0      |  -20.0417306018256  |  -1.23597368422708  |
    |     0      |  -21.2643719493711  |  -2.48245567897449  |
    |     0      |  -21.4825583139819  |  -2.06515697160044  |
    |     0      |  -24.8407334321368  |   -1.3013539259794  |
    |     0      |  -24.0034272423961  |  -1.54027947063571  |
    |     0      |  -24.1021895544148  |  -0.289140839729988 |
    |     0      |   -22.081457496193  |  -1.04527444394551  |
    |     0      |  -23.9625342651096  |  -0.15668995918552  |
    |     0      |  -22.1433063024391  |  -1.35383849328097  |
    |     0      |  -24.1870727619096  |  -0.215292128368883 |
    |     0      |   -23.86260162986   |  -0.955005560980645 |
    |     0      |  -24.4228204476753  |  -0.653666805314675 |
    |     0      |  -23.8480480382443  |  0.435449008567002  |
    |     0      |  -11.1242906591502  |   -18.42754445664   |
    |     0      |  -11.6875175324676  |  -18.6532018676648  |
    |     0      |  -13.3487045943498  |  -20.8078101490661  |
    |     0      |  -12.3298505727806  |  -20.4510720891185  |
    |     0      |  -11.9841956007221  |  -20.5933479571684  |
    |     0      |  -10.9648210396826  |  -19.3134071278914  |
    |     0      |  -12.7917047765999  |  -20.9674659166334  |
    |     0      |  -12.2909186348742  |  -21.3500649185619  |
    |     0      |  -12.2605410345181  |  -21.2764082226327  |
    |     0      |   -10.675409266574  |  -20.0286170677415  |
    |     0      |   -10.71341842679   |  -19.4344953375098  |
    |     0      |  -20.8246728153083  |  0.730694493153454  |
    |     0      |  -21.3774869900092  |   0.59351745322045  |
    |     0      |  -22.6296127762783  |  0.980059092855107  |
    |     0      |   -22.255044033404  |   1.12144871434264  |
    |     0      |  -23.5695823089078  |   1.41466081906793  |
    |     0      |  -24.6392098719437  |   1.80086194388608  |
    |     0      |  -21.6994950998106  |  0.743950775705255  |
    |     0      |  -23.5309844829752  |   2.55857437269696  |
    |     0      |  -23.8872266136516  |   2.41888390268147  |
    |     0      |  -21.9491436597654  |   1.99962785793451  |
    |     0      |  -9.93447333338413  |  -18.6162807250471  |
    |     0      |  -9.60530924359584  |  -20.1065218518984  |
    |     0      |   -9.3795805863941  |  -19.9773953272856  |
    |     0      |   -9.292625977794   |  -18.1518878290206  |
    |     0      |   -10.221155679422  |  -17.9895595149088  |
    |     0      |  -9.60728765214201  |  -20.2597773378993  |
    |     0      |  -9.15430757876221  |  -19.7537707373285  |
    |     0      |  -11.9572453372913  |  -21.7142362830761  |
    |     0      |  -9.67725933747239  |  -20.8495107692897  |
    |     0      |  -8.36273957200476  |   -19.862384579546  |
    |     0      |  -8.71419237633897  |  -21.5308984026922  |
    |     0      |  -9.21215051049932  |  -21.6380794516942  |
    |     0      |  -20.8017115461648  |   2.7006253496281   |
    |     0      |  -20.9547692658169  |   1.77529990988565  |
    |     0      |  -20.6137342358072  |   1.67021273014612  |
    |     0      |  -20.0520459539499  |   2.4946231523038   |
    |     0      |  -21.0242426004374  |   1.94169738187534  |
    |     0      |  -22.8913215212018  |    3.749982304289   |
    |     0      |  -23.8149483216996  |   4.44688884515636  |
    |     0      |  -20.2187935799448  |   3.62432712159321  |
    |     0      |  -20.2537482582283  |   3.68145484415882  |
    |     0      |  -7.65004105989357  |  -19.1788956030174  |
    |     0      |  -8.10333126369088  |  -19.1647122354082  |
    |     0      |  -7.83970627600313  |  -21.4235868055483  |
    |     0      |  -7.89558528126012  |  -21.4454069251406  |
    |     0      |  -7.49026105389477  |  -20.9246786757953  |
    |     0      |  -7.62070216360535  |  -20.9707762561602  |
    |     0      |  -7.08211219500848  |  -18.7625782535237  |
    |     0      |  -7.67965423068016  |  -21.9173226025502  |
    |     0      |  -8.98231057635616  |  -22.7712992801197  |
    |     0      |  -6.44594525520035  |   -19.510419361531  |
    |     0      |  -6.45293513380593  |  -19.7889502135985  |
    |     0      |  -6.38918167976159  |  -22.4289342050575  |
    |     0      |  -21.3788576174429  |   4.60490662586173  |
    |     0      |  -22.1317799515705  |   5.64309562586392  |
    |     0      |  -21.9074032022187  |   5.28449990334199  |
    |     0      |  -23.6400984919817  |   5.08822904903825  |
    |     0      |  -23.3662871403463  |   5.86754364467577  |
    |     0      |  -24.3266685862684  |   5.5648807345726   |
    |     0      |  -24.0283254762312  |   5.37785246520203  |
    |     0      |   -22.542908344205  |   6.40521218599994  |
    |     0      |  -20.3773295485309  |   5.76931947412404  |
    |     0      |  -6.54430530571579  |   -23.370202141055  |
    |     0      |  -6.42087051245424  |  -22.7436265897675  |
    |     0      |  -4.81453762846744  |  -21.0715051722114  |
    |     0      |  -4.32909504944882  |   -22.557334367911  |
    |     0      |   -5.4143704149939  |   -23.606896050557  |
    |     0      |  -22.4544580781155  |   6.81183230216235  |
    |     0      |  -21.0329888835703  |   6.08265659822275  |
    |     0      |  -20.4079370458647  |   6.80582555095005  |
    |     0      |  -20.7170397023284  |   6.18211481775256  |
    |     0      |  -22.3766526427943  |   6.53453265853903  |
    |     0      |  -23.4215592492472  |   7.7618055663825   |
    |     0      |   -23.459780285349  |   7.19324614954797  |
    |     0      |  -23.5598772524669  |   7.57697628931002  |
    |     0      |   -21.885771722014  |   7.53910743283998  |
    |     0      |  -21.6746018485514  |   8.54633622036611  |
    |     0      |  -22.9334446126285  |   8.72800994372368  |
    |     0      |  -18.7878726486992  |   7.67558507280219  |
    |     0      |  -19.9944667261999  |   6.98148907720181  |
    |     0      |  -19.6908849499612  |   7.53485734226874  |
    |     0      |   -19.595663572939  |   7.20057128099752  |
    |     0      |  -19.1311308155447  |   7.52992119292259  |
    |     0      |  -3.51188517106319  |  -22.8300100182323  |
    |     0      |  -3.90769558907845  |  -21.5036972875258  |
    |     0      |  -3.65384555359084  |  -20.3272858380001  |
    |     0      |  -2.49544194782872  |  -21.8201694296767  |
    |     0      |   -2.4044735717608  |  -21.1269725561733  |
    |     0      |  -3.40237362701556  |  -20.4467190408365  |
    |     0      |  -3.79502953905381  |  -22.0005676136355  |
    |     0      |  -3.10559201897382  |  -24.5756631482279  |
    |     0      |  -3.25904468924694  |   -24.649997567595  |
    |     0      |  -3.40591092985399  |  -24.3260414569294  |
    |     0      |  -2.45923329026403  |  -22.3901258769399  |
    |     0      |  -2.94060391743695  |   -22.867945301285  |
    |     0      |  -20.4697394023974  |   8.83717715453225  |
    |     0      |  -18.8787145744444  |   7.88381320093004  |
    |     0      |  -22.8535844701592  |   9.84154599012879  |
    |     0      |   -21.29864718127   |   9.35588650608244  |
    |     0      |  -21.9691005055649  |   10.8327944929864  |
    |     0      |  -20.0149179413053  |   9.69264799947508  |
    |     0      |  -18.6772313638019  |   8.74084182257803  |
    |     0      |  -18.3124610191735  |   8.66320667958968  |
    |     0      |  -2.09156860461997  |  -24.7527965808999  |
    |     0      |  -1.62800533074327  |  -24.4513702110627  |
    |     0      |  -2.39091668156484  |  -24.4834295704418  |
    |     0      |   -1.4340762172053  |  -22.7514428076108  |
    |     0      |  -0.608377775926318 |  -21.9712018952571  |
    |     0      |  -1.32294906132061  |  -24.8413366730517  |
    |     0      |  -0.108156388210208 |  -23.0731302397666  |
    |     0      |  -19.4393218003397  |   10.4696181069452  |
    |     0      |  -21.4262813080225  |   11.5544270428617  |
    |     0      |  -20.7732373363214  |   11.7109333335939  |
    |     0      |  -21.1456222907387  |   11.9984612972468  |
    |     0      |   -21.124165130837  |   12.2510472951695  |
    |     0      |  -17.4936477525596  |   10.4115538696812  |
    |     0      |  0.616507453665371  |  -21.5316685831787  |
    |     0      |   1.62911185837775  |  -21.6752127961606  |
    |     0      |   1.37826103082777  |  -22.1372048124379  |
    |     0      |   1.52562992951163  |  -24.5926055822487  |
    |     0      |   1.77979745286507  |   -23.375743324112  |
    |     0      |  -18.1635895712132  |   11.7876524509805  |
    |     0      |  -18.9017947269146  |   12.8271869094238  |
    |     0      |  -20.6035619348304  |   13.0269023999697  |
    |     0      |  -19.3651254728274  |   13.3127090932395  |
    |     0      |  -16.5230296512707  |   11.2815177237063  |
    |     0      |  -16.1128753522005  |   12.2063662564412  |
    |     0      |   1.63234997383894  |  -20.2407168900784  |
    |     0      |   2.21604466308655  |  -20.4937022856873  |
    |     0      |   2.2047091634966   |  -20.4736875116237  |
    |     0      |   3.81619228460648  |  -20.5464491367091  |
    |     0      |   2.33930017675241  |  -23.6420395777757  |
    |     0      |   3.11917505605108  |   -20.851771694539  |
    |     0      |   3.43817790431817  |   -22.900861407584  |
    |     0      |   2.4201644479391   |  -23.9094419399786  |
    |     0      |   3.31639455552976  |  -23.0693121664549  |
    |     0      |   3.76399214321934  |  -23.1504788380817  |
    |     0      |  -17.3646953387022  |   14.4241754614861  |
    |     0      |  -19.2067285274187  |   15.2223397466458  |
    |     0      |  -17.6630975411567  |   14.3920732147023  |
    |     0      |  -19.2040803349596  |   14.6581914460557  |
    |     0      |  -17.4022663582127  |   14.3267069893548  |
    |     0      |  -15.4349648116319  |   12.919139507189   |
    |     0      |   5.69780044290135  |  -19.3896078944158  |
    |     0      |   5.35512360760715  |   -22.092798071491  |
    |     0      |   5.63090465992266  |  -21.6854606041151  |
    |     0      |   5.27079220873806  |  -20.3798638635221  |
    |     0      |   4.43767496824156  |  -21.9161998699029  |
    |     0      |   4.40274571506435  |  -24.0224944655888  |
    |     0      |   5.80826547500131  |   -22.171974180812  |
    |     0      |   4.90302542685672  |  -23.6143060953423  |
    |     0      |   -16.499927589437  |   15.9473178167582  |
    |     0      |  -16.0475939004904  |   16.4522295545098  |
    |     0      |  -17.5671442144397  |   15.102524119477   |
    |     0      |  -16.5741747671618  |   16.5546524066267  |
    |     0      |   -14.60212592017   |   14.5650589091541  |
    |     0      |  -13.8928203326151  |   14.7518329507447  |
    |     0      |   7.77387764899706  |  -18.5775184042647  |
    |     0      |   7.35616585349486  |  -19.0028199665262  |
    |     0      |   8.07339445830947  |  -19.8987773363007  |
    |     0      |   7.84991680777162  |  -21.9631114261984  |
    |     0      |   7.65885023058338  |   -23.026561526594  |
    |     0      |   7.74432238319159  |  -22.5774382928281  |
    |     0      |   7.01483852789497  |  -21.6779755412964  |
    |     0      |   7.9964496348968   |  -22.2525003586209  |
    |     0      |  -16.0408478188519  |   17.4678102566245  |
    |     0      |  -16.8940401831148  |   18.0839195349645  |
    |     0      |  -17.3941925831112  |   17.286829530395   |
    |     0      |  -15.3268064094367  |   17.325311034138   |
    |     0      |   -17.11492333194   |   17.3466532222678  |
    |     0      |  -15.4383675383583  |   17.9223737180803  |
    |     0      |  -15.0083229830527  |   15.4063405890047  |
    |     0      |  -15.3610031308425  |   18.1019936656123  |
    |     0      |  -15.7534461658231  |   17.0963603035064  |
    |     0      |   -15.761133465339  |   17.4523383111005  |
    |     0      |  -15.9740343182227  |   18.4997956936712  |
    |     0      |  -13.9199932752736  |   16.2330856505936  |
    |     0      |  -16.3119147956892  |   18.8861150033242  |
    |     0      |  -14.3761114633531  |   17.3820817807606  |
    |     0      |   9.80689115114831  |  -19.7235580974834  |
    |     0      |   8.66069241131689  |  -21.0009035402913  |
    |     0      |   10.2710684925649  |   -19.275810124481  |
    |     0      |   10.5173555833834  |  -19.6466053345458  |
    |     0      |   10.3348841822403  |  -20.1969974884749  |
    |     0      |   10.1931677829442  |  -22.1734869047876  |
    |     0      |   9.88989769708827  |  -22.5805970596059  |
    |     0      |   8.88750687422581  |  -22.6393181586821  |
    |     0      |  -14.2782776566587  |   18.5064089454275  |
    |     0      |  -14.6192128488883  |   19.4650493070786  |
    |     0      |  -14.8095305263109  |   18.631260420024   |
    |     0      |   -15.273487423674  |   19.3035681705473  |
    |     0      |  -13.1360793198161  |   18.4191106555141  |
    |     0      |   -13.326099812205  |   18.7158790154922  |
    |     0      |  -14.2708639564323  |   19.3892048412884  |
    |     0      |  -13.8249038433772  |   19.1459424533629  |
    |     0      |  -14.4261536604847  |   19.6079916528463  |
    |     0      |   -14.400740917493  |   19.9885810236393  |
    |     0      |   -13.134421356085  |   18.9019684418579  |
    |     0      |   11.0138557087695  |  -19.1923366599681  |
    |     0      |   10.5658350910832  |  -21.8467937302062  |
    |     0      |   11.2882893003003  |  -19.3809288294897  |
    |     0      |   11.3277708582244  |  -20.7970082973116  |
    |     0      |   11.1308770888163  |  -21.1882887390388  |
    |     0      |   11.7802270393727  |  -18.1872764337749  |
    |     0      |   10.8482018978559  |  -17.3077525302338  |
    |     0      |   12.4352690705262  |  -19.7385070588153  |
    |     0      |   12.209648376894   |  -17.9203884643132  |
    |     0      |   11.4899482980789  |  -21.6394687288625  |
    |     0      |   12.4790262838262  |  -21.0667480929134  |
    |     0      |   12.6934825618255  |  -18.6005584865811  |
    |     0      |   11.3738302776468  |  -22.0675158766413  |
    |     0      |   12.6713580860157  |  -20.9831192139458  |
    |     0      |  -11.8177782915615  |   18.5454653313129  |
    |     0      |  -12.8446057382247  |   19.6907689071683  |
    |     0      |   -13.963893865684  |   20.5255738904353  |
    |     0      |  -12.7826282697649  |   20.7298268544161  |
    |     0      |  -10.8010088725952  |   19.2557136268614  |
    |     0      |   12.8458164808554  |  -18.6338072380208  |
    |     0      |   13.3034563103241  |  -19.3707667264951  |
    |     0      |   13.4748306304565  |  -16.4539512439882  |
    |     0      |   13.8154453778711  |  -16.8555104601455  |
    |     0      |   14.2277645595501  |  -17.8653554026342  |
    |     0      |   14.2290266413377  |  -18.6086646484251  |
    |     0      |   14.1154439836347  |  -17.3344093572043  |
    |     0      |   13.8965337019863  |  -19.4330211004396  |
    |     0      |   13.7907602073582  |  -19.4470199963297  |
    |     0      |   14.6928838639021  |  -19.5041794769951  |
    |     0      |   14.0706217331209  |  -19.5371376325084  |
    |     0      |   14.4950439173239  |  -19.5434548866672  |
    |     0      |   15.1299828617508  |  -18.3314948544519  |
    |     0      |   15.1346830372394  |  -18.8117052632439  |
    |     0      |  -9.56482146147863  |   19.2922794699167  |
    |     0      |  -10.9638624759223  |   20.4246213405508  |
    |     0      |   -9.8665576590535  |   18.502300555586   |
    |     0      |  -11.0173800895072  |   21.353435374961   |
    |     0      |   -11.510600865125  |   21.4031635534033  |
    |     0      |  -11.5940164013738  |   21.142319983869   |
    |     0      |   -10.778978669913  |   21.2311637803126  |
    |     0      |   -11.472664022107  |   22.1321864273083  |
    |     0      |  -10.5984796004363  |   20.986487551586   |
    |     0      |  -10.8428587372614  |   22.2596552443037  |
    |     0      |  -10.5560710586403  |   21.4839501057211  |
    |     0      |  -11.3958282100017  |   21.7586146652506  |
    |     0      |  -9.06126500762127  |   17.9945210427952  |
    |     0      |  -8.64926473407506  |   19.5392885685616  |
    |     0      |  -9.03425004055456  |   20.5414839533817  |
    |     0      |  -8.95132752319394  |   18.4721215364859  |
    |     0      |   15.5644959493375  |  -16.7650292123505  |
    |     0      |   15.6297459689107  |  -16.8444367087653  |
    |     0      |   15.1158853853661  |  -15.8801150000096  |
    |     0      |   15.542406304992   |  -16.8124559297284  |
    |     0      |   15.3264807957814  |   -16.026028008678  |
    |     0      |   15.5622955600556  |  -17.3719433566425  |
    |     0      |   16.2879222963415  |   -16.809799285517  |
    |     0      |   16.1907537333624  |  -16.6795073503999  |
    |     0      |   16.030051974128   |  -16.1052003694257  |
    |     0      |  -9.01517799776754  |   21.0897334600285  |
    |     0      |  -7.33166047480501  |   20.176383315202   |
    |     0      |  -8.30963071589807  |   21.4081059891768  |
    |     0      |  -7.52449162887618  |   20.0555813708601  |
    |     0      |  -7.40131730325581  |   19.1409447435946  |
    |     0      |  -8.64567704668533  |   20.8391123431917  |
    |     0      |  -9.21195779657548  |   22.0676004407311  |
    |     0      |  -10.3641256854702  |   22.2977790503287  |
    |     0      |  -9.65637536004948  |   22.2166885841716  |
    |     0      |  -9.09606932387504  |   22.6250664785621  |
    |     0      |  -9.73347427078219  |   22.7603109077366  |
    |     0      |  -8.10766461450032  |   22.3032253083322  |
    |     0      |  -7.79165247585236  |   22.2965395531135  |
    |     0      |   15.6495501010909  |  -15.1554675494113  |
    |     0      |   15.9730900269808  |  -15.0249924231437  |
    |     0      |   17.4547324387611  |  -15.3390137200891  |
    |     0      |   16.5853554110906  |  -15.5967754035242  |
    |     0      |   18.2127597244516  |  -16.2114210153052  |
    |     0      |  -5.01406783238708  |   20.2863875521749  |
    |     0      |  -5.93044030523414  |   21.6329527071831  |
    |     0      |  -5.70743113323461  |   19.803149623239   |
    |     0      |  -6.13804929011411  |   20.8930346164354  |
    |     0      |  -6.37276888888924  |   23.3912592047785  |
    |     0      |   -5.6828680823943  |   22.4259172554249  |
    |     0      |  -5.58460477301134  |   22.6267289359247  |
    |     0      |   16.2522495450695  |  -12.6817162324124  |
    |     0      |   18.9277575323022  |  -15.0324181607144  |
    |     0      |   19.1827870878311  |  -15.5562996354682  |
    |     0      |   19.1008658120878  |  -15.1280662464574  |
    |     0      |  -4.65580480157202  |   21.5418207443048  |
    |     0      |  -4.01061006309959  |   20.4290088012018  |
    |     0      |  -4.87806227983817  |   22.1625289866526  |
    |     0      |   -4.3249033760861  |   20.3477882059979  |
    |     0      |  -4.49876707489545  |   23.4420737477215  |
    |     0      |  -3.35440287755542  |   23.2990003648675  |
    |     0      |   18.2077104892618  |  -12.3352316382039  |
    |     0      |   17.7608725348305  |  -11.1697814828575  |
    |     0      |   17.4989654414817  |  -12.6951955434378  |
    |     0      |   18.110967726964   |  -11.4543568047017  |
    |     0      |   16.961332872492   |   -11.863902461186  |
    |     0      |   19.6893791410557  |  -13.9156962227615  |
    |     0      |  -2.40633128090125  |   21.6902731436725  |
    |     0      |  -2.07554964678155  |   20.5914079889615  |
    |     0      |  -2.32432003939725  |   19.9408335820496  |
    |     0      |  -3.65527082637664  |   24.3405964920952  |
    |     0      |  -1.63981014706185  |   24.4042092232985  |
    |     0      |  -1.40903823841784  |   22.4050045001344  |
    |     0      |   -1.5201033915021  |   22.5116481061613  |
    |     0      |   18.3109908799226  |   -10.60602107812   |
    |     0      |   20.4948852283391  |   -11.698077030805  |
    |     0      |   17.8140170140257  |  -10.3380622972446  |
    |     0      |   18.7535333650902  |  -10.5251543156454  |
    |     0      |   19.028543468578   |  -10.1850674884324  |
    |     0      |   19.2032718538322  |  -10.8802869850212  |
    |     0      |   19.4456135362599  |  -11.4784885833405  |
    |     0      |   20.1835555933339  |  -12.0871269316818  |
    |     0      |   20.0392955425378  |  -12.1805783999993  |
    |     0      |   18.9717193338888  |  -11.6595197639705  |
    |     0      |   17.2853386226508  |  -10.1573337498854  |
    |     0      |   19.8065348876671  |   -10.482485958134  |
    |     0      |   18.5259100252417  |  -9.56698944073496  |
    |     0      |   18.2784810165309  |  -8.92215298205715  |
    |     0      |   21.3506779150808  |  -12.2677026490065  |
    |     0      |   20.9851219998603  |  -13.2070215364019  |
    |     0      |   20.8213034299301  |  -12.6691041689688  |
    |     0      |   -1.4378994127912  |   20.9024982973479  |
    |     0      | 0.00321565894559939 |   21.3948051428398  |
    |     0      |  -0.726728199853902 |   21.4492546610764  |
    |     0      |  -0.755064504107025 |   22.8346912645896  |
    |     0      |  0.101631938061509  |   21.7980036031446  |
    |     0      |  0.774682837433499  |   23.9319985960294  |
    |     0      |  0.176153832662923  |   23.7736743869137  |
    |     0      |  -0.501104200026532 |   23.6071688349392  |
    |     0      |  -0.172018015371645 |   23.2263831413474  |
    |     0      |  -0.250753166736452 |   24.2221708638697  |
    |     0      |  -0.157062185535704 |   24.0533318599003  |
    |     0      |  -0.793815905132245 |   24.4765128239414  |
    |     0      |  0.271201541307942  |   23.3393286812768  |
    |     0      |  0.382876710678858  |   22.1739945687233  |
    |     0      |    20.0215740339    |  -9.09815162145447  |
    |     0      |   20.3070516443379  |  -9.18882427932174  |
    |     0      |   19.8110668895818  |   -9.4677505942377  |
    |     0      |   20.0680036307629  |  -9.40209335386851  |
    |     0      |   21.6656320247173  |  -11.1089966195212  |
    |     0      |   21.0919001819994  |  -10.7058973450707  |
    |     0      |   20.8796393107062  |  -9.58356532947326  |
    |     0      |   21.8388421213435  |  -10.0702314335249  |
    |     0      |   21.9165088361672  |  -11.0914271725767  |
    |     0      |   20.3983792082399  |   -8.6671990033552  |
    |     0      |   20.4826597801795  |  -8.35879050817284  |
    |     0      |   21.5482016543617  |  -9.13209870184404  |
    |     0      |   19.3351103897836  |  -6.66493195186599  |
    |     0      |   1.33179099128199  |   20.5941399538862  |
    |     0      |   2.20528721213587  |   22.0062655382819  |
    |     0      |   1.36803569103034  |    21.39099209867   |
    |     0      |   1.83627366872331  |   20.8041620421243  |
    |     0      |   1.35157926769535  |    20.55429413242   |
    |     0      |   1.20829205317809  |   24.171414691569   |
    |     0      |   1.56980598185668  |   23.3900325830979  |
    |     0      |   2.91993791606274  |   24.4188484034589  |
    |     0      |   21.2453327124218  |  -7.35723738668358  |
    |     0      |   21.763128855621   |  -8.28771408800395  |
    |     0      |   21.0994714620055  |  -8.06263880015474  |
    |     0      |   22.3227788448905  |  -9.72464710228362  |
    |     0      |   22.7878808964919  |  -9.12133724620628  |
    |     0      |   22.8653292161717  |  -10.0351537973784  |
    |     0      |   21.2547335057774  |  -6.84917791832666  |
    |     0      |   22.0287826364063  |   -6.4373506845149  |
    |     0      |   23.1714379033872  |  -7.56946547542208  |
    |     0      |   20.2553476184864  |  -5.42264584471595  |
    |     0      |   20.3773319699696  |  -4.49777179374256  |
    |     0      |   21.142683455787   |  -4.97588297816733  |
    |     0      |   20.3484399222529  |  -5.60479940874725  |
    |     0      |   19.558782477192   |  -4.88062949379935  |
    |     0      |   19.9576498684276  |  -5.20734669650316  |
    |     0      |   19.3533401677168  |  -5.88314695324895  |
    |     0      |   19.8588796401671  |  -4.59798193983639  |
    |     0      |   4.16206958664678  |   21.4728791250255  |
    |     0      |   22.4441279645283  |   -5.3470413807533  |
    |     0      |   22.3921286628545  |  -6.67273485179652  |
    |     0      |   23.544649825685   |   -6.8175758150488  |
    |     0      |   22.2686199225805  |  -5.73815786314111  |
    |     0      |   23.0087881665718  |  -5.02392369323593  |
    |     0      |   24.1247065594069  |  -5.27561923036148  |
    |     0      |   24.2168792985458  |  -5.85668875410067  |
    |     0      |   23.9235103125328  |  -5.84140912668845  |
    |     0      |   19.7807260299012  |  -3.53029192356872  |
    |     0      |   19.6815483014479  |  -4.14836449974606  |
    |     0      |   22.3852972487851  |  -3.87058878730544  |
    |     0      |   22.1985261874267  |  -3.52053264087091  |
    |     0      |   22.3635908669623  |  -3.19161046212148  |
    |     0      |   4.96214869430388  |   20.2974366002238  |
    |     0      |   4.57549571505538  |   20.5175004878629  |
    |     0      |   5.08433165032618  |   21.1832556855787  |
    |     0      |   4.66414023175097  |   19.5052300321428  |
    |     0      |    5.523995696811   |   21.801308354736   |
    |     0      |   5.2357583447526   |   19.6176067668095  |
    |     0      |   5.36074535006692  |   23.6434255254657  |
    |     0      |   24.1371727078861  |  -4.54715156440956  |
    |     0      |   24.3653899987067  |  -3.90479589295797  |
    |     0      |   24.0972175258664  |  -3.20134357465493  |
    |     0      |   24.4539675300261  |  -3.17052247848851  |
    |     0      |    22.57981297913   |  -2.42799507799931  |
    |     0      |   23.9212907380058  |  -2.21602848135681  |
    |     0      |   23.8317012082933  |  -1.90964172450343  |
    |     0      |   24.0109108150987  |   -2.5043470214607  |
    |     0      |   22.9836656004114  |  -1.42475798559597  |
    |     0      |   21.3932194031743  |  -1.42836027146706  |
    |     0      |   22.7358157270289  |  -1.28907034000804  |
    |     0      |   23.7802409328428  |  -1.65890221328424  |
    |     0      |   23.8125693280308  |  -1.18486097836162  |
    |     0      |   23.7249417923041  |  -1.47291646640418  |
    |     0      |   6.76867337048457  |   21.0353254554958  |
    |     0      |   5.56204106219208  |   19.2334772759273  |
    |     0      |   6.19292670450775  |   19.9970315652886  |
    |     0      |   6.44152626928013  |   22.8781778588324  |
    |     0      |   7.04266453722616  |   22.9475480960438  |
    |     0      |   7.63058181974598  |   23.0450805966021  |
    |     0      |   6.63248332293354  |   23.2240343923792  |
    |     0      |   6.69718600422944  |   23.5144671744269  |
    |     0      |   7.61573723639163  |   19.0207293229274  |
    |     0      |   24.440522724502   |   -1.1174141783814  |
    |     0      |   24.804856022729   |  -0.710054010017799 |
    |     0      |   21.4511180978506  |  -0.761460082494402 |
    |     0      |   24.9336519511108  | 0.00882261665948647 |
    |     0      |   23.5230207902021  |  0.399537722300526  |
    |     0      |   21.6938704702509  |  0.610260630776295  |
    |     0      |   20.3582927795864  |  -0.451421004464581 |
    |     0      |   21.2384646508091  |  0.724577473348276  |
    |     0      |   20.2388417884888  |  0.350545242126355  |
    |     0      |   22.1371761742687  |   1.00670853909418  |
    |     0      |   24.5515899032129  |  0.723817653825421  |
    |     0      |   23.9753887285364  |  0.889823481389239  |
    |     0      |   8.79086353061295  |   22.2060085494099  |
    |     0      |   8.46467517943339  |   20.8447696388908  |
    |     0      |   8.61670530103925  |   20.5991763368245  |
    |     0      |   8.01798449038434  |   21.0224929712818  |
    |     0      |   7.96221160933479  |   22.7268236213023  |
    |     0      |   8.68693377528663  |   20.4364765879868  |
    |     0      |   8.4428633718951   |   20.2284154692797  |
    |     0      |   8.32359135771338  |   20.7678947810865  |
    |     0      |   8.20500030331547  |   19.168695618477   |
    |     0      |   8.73291896829983  |   20.2392140614051  |
    |     0      |   9.16179178010756  |   22.8756615416499  |
    |     0      |   9.70166965141039  |   21.8419561147885  |
    |     0      |   8.51242625318115  |   18.7756910891159  |
    |     0      |   9.75337819417631  |   18.4000172854401  |
    |     0      |   9.28648732802201  |   19.5334967200335  |
    |     0      |   9.10434747771562  |   18.6314775578824  |
    |     0      |   10.0431214482724  |   19.6071360467966  |
    |     0      |   8.53287451133731  |   18.3140906939814  |
    |     0      |   9.93373775153129  |   18.8333688275113  |
    |     0      |   24.4328502562981  |   2.31647306462586  |
    |     0      |   22.5763238489518  |   2.03277050844988  |
    |     0      |   22.3255686915133  |   2.51647412195637  |
    |     0      |   20.7975486041035  |   2.60964260790946  |
    |     0      |   21.5084997455163  |   2.0269082519351   |
    |     0      |   23.3731491250792  |   3.06629949624944  |
    |     0      |   10.299689083034   |   21.2410434597363  |
    |     0      |   10.1018422679519  |   20.7806593951679  |
    |     0      |   10.1104390738115  |   22.5067731214253  |
    |     0      |   10.8460523122205  |   20.9856518059902  |
    |     0      |   10.8311693816591  |   20.7241987789628  |
    |     0      |   10.5838331326767  |   19.0402315203288  |
    |     0      |   10.3166723322667  |    17.29325388665   |
    |     0      |   10.8182583403859  |   18.3210874643741  |
    |     0      |   11.9821690893649  |   18.9327690489277  |
    |     0      |   10.9639384718444  |   17.3368655342315  |
    |     0      |   11.5225712473144  |   17.9058522185804  |
    |     0      |   10.9311447646148  |   17.4393620073979  |
    |     0      |   11.2718070327639  |   17.6802185097152  |
    |     0      |   12.3362877580041  |   20.0688336720079  |
    |     0      |   12.3851201438276  |   19.1188530037733  |
    |     0      |   11.7667440961892  |   20.0340712885531  |
    |     0      |   12.276566674596   |   18.8830910687722  |
    |     0      |   22.9211363931751  |   4.23764983622248  |
    |     0      |   23.2789618420782  |   3.52536832379427  |
    |     0      |   23.3141512834999  |   3.48790766600888  |
    |     0      |   21.7174972392234  |   3.48436391376162  |
    |     0      |   20.4779603730319  |   3.67204545935245  |
    |     0      |   19.5283480428757  |   4.56296847181533  |
    |     0      |   20.9142570830482  |   4.89331068466106  |
    |     0      |   20.0454722834031  |   4.96641638687179  |
    |     0      |   20.4359009840693  |   4.94904382151973  |
    |     0      |   24.4959016095362  |   4.81843826352546  |
    |     0      |   22.1017332268421  |   5.20556791695094  |
    |     0      |   23.2455846845385  |   5.55075464330183  |
    |     0      |   12.766144046451   |   20.003038363067   |
    |     0      |   11.6190051364801  |   16.3380257744985  |
    |     0      |   12.0781822069912  |   16.4823617280844  |
    |     0      |   12.8957667331657  |   17.0707364762531  |
    |     0      |   13.0978521602684  |   17.9099736236548  |
    |     0      |   12.9814033806237  |   18.0279051386881  |
    |     0      |   13.7361493607686  |   17.1692049094332  |
    |     0      |   14.1339528323775  |   19.4064963117272  |
    |     0      |   13.3967023055985  |   17.4262255162123  |
    |     0      |   13.7766872713234  |   19.8166568739417  |
    |     0      |   14.1982587236903  |   19.1403623410223  |
    |     0      |   12.7543372277889  |   15.5925331593456  |
    |     0      |   14.1443079286927  |   20.3870037549115  |
    |     0      |   14.5594042444413  |   19.209677700051   |
    |     0      |   14.8408708115299  |   19.1313462770224  |
    |     0      |   23.2840141739156  |   5.71997395284473  |
    |     0      |   24.2960809726715  |   5.67731593301395  |
    |     0      |   22.8950559384632  |   6.72714090055187  |
    |     0      |   19.4561917076149  |   5.44234296793227  |
    |     0      |   19.731164278803   |   5.66846473639294  |
    |     0      |   21.3462658442307  |   6.21498787366552  |
    |     0      |   19.9909229041035  |   6.20324440822156  |
    |     0      |   21.852232095251   |   6.49875632091367  |
    |     0      |   20.9675635890884  |   6.90040692309868  |
    |     0      |   23.1387146041443  |   7.33158436246756  |
    |     0      |   23.1672046464715  |   7.85127919300053  |
    |     0      |   15.0349089829414  |   18.9556275000589  |
    |     0      |   14.1020331481015  |   16.6141780054263  |
    |     0      |   14.2186340592888  |   17.1440132158548  |
    |     0      |   14.164980472608   |   16.9809314152137  |
    |     0      |   14.4769049899079  |   16.843898776846   |
    |     0      |   14.3955142653526  |   17.2793008351136  |
    |     0      |   14.2114476250538  |   16.7360140437894  |
    |     0      |   14.7029568160432  |   16.4264201845165  |
    |     0      |   14.8773155128012  |   16.2312650313746  |
    |     0      |   15.2029378992519  |   19.2455574610483  |
    |     0      |   15.7020144354096  |   18.1569107543476  |
    |     0      |   14.0017096134842  |   14.690739097861   |
    |     0      |   14.045155369232   |   14.7499350783182  |
    |     0      |   15.4213323911751  |   16.4409651846816  |
    |     0      |   23.5222161973464  |   8.41912975694012  |
    |     0      |   20.9842792460622  |   7.53272209900093  |
    |     0      |   21.2084031413348  |   7.93734816039789  |
    |     0      |   20.9779346575858  |   8.21354360469316  |
    |     0      |   21.033560948462   |   8.01707160799628  |
    |     0      |   19.704314505078   |   7.76463247964374  |
    |     0      |   18.5675345098449  |   7.5133506592891   |
    |     0      |   18.8659042789908  |   8.43549523662566  |
    |     0      |   19.8304877126731  |   8.72145981235498  |
    |     0      |   22.300354646193   |   9.47273419446905  |
    |     0      |   16.7397622446249  |   17.254710892334   |
    |     0      |   16.1310051526553  |   16.3075367181131  |
    |     0      |   16.1095245699908  |   16.0000985213556  |
    |     0      |   16.416884163123   |   15.524863424024   |
    |     0      |   16.7310402690112  |   14.7164154982736  |
    |     0      |   17.3142729989785  |   17.0816558143504  |
    |     0      |   17.1917728112041  |   17.5082006456834  |
    |     0      |   14.7537635591597  |   13.7096960044977  |
    |     0      |   15.5487076568178  |   12.8402345990018  |
    |     0      |   16.5320793127325  |   14.2041719701161  |
    |     0      |   17.4035867873596  |   15.0791475735973  |
    |     0      |   19.870750044878   |   9.59723048591857  |
    |     0      |   20.0123386899998  |   10.4377778644849  |
    |     0      |   17.6357040613125  |   9.66237992265373  |
    |     0      |   19.3787672763591  |   10.2464124724485  |
    |     0      |   17.4930707516582  |   10.4394251180065  |
    |     0      |   20.6543762682259  |    11.14443532943   |
    |     0      |   22.3262789879582  |   11.0838241111878  |
    |     0      |   21.461524230643   |   11.5843082482853  |
    |     0      |   18.0326727652143  |   16.0102804149549  |
    |     0      |   16.9970308626057  |   13.9083196357397  |
    |     0      |   18.7082634045315  |   15.279719764497   |
    |     0      |   18.7285727093595  |   14.5941511213752  |
    |     0      |   18.5581147407918  |   15.2023231797862  |
    |     0      |   17.4549219629052  |   12.723718135489   |
    |     0      |   19.0060458118124  |   14.1892641499589  |
    |     0      |   16.3422466448239  |   12.9280742201619  |
    |     0      |   16.8508106571859  |   12.4176863755182  |
    |     0      |   16.3735695841599  |   12.4961267865711  |
    |     0      |   19.0186577355576  |   15.8435494596341  |
    |     0      |   19.0229099448877  |   15.7873316857905  |
    |     0      |   17.4004361230882  |   11.4321392897666  |
    |     0      |   17.0918227835055  |   12.1202571257578  |
    |     0      |   17.0250934744371  |   11.0886550210829  |
    |     0      |   17.3401708911826  |   12.2147286251256  |
    |     0      |   19.2009432214317  |   13.9189466083976  |
    |     0      |   18.9454368287443  |   11.6846097571238  |
    |     0      |   19.5518277560136  |   11.9164274246043  |
    |     0      |   19.622835980087   |   12.3590553120519  |
    |     0      |   20.857703474284   |   11.953739908968   |
    |     0      |   18.5003879915459  |   11.7080483989362  |
    |     0      |   21.1789589357464  |   12.6165258873331  |
    |     0      |   17.2969172207159  |   10.4904369849202  |
    |     0      |   21.7481642015037  |   12.3236240527237  |
    |     0      |   20.029704433414   |   14.6794602692497  |
    |     0      |   20.2799642669409  |   14.0966170649494  |
    |     1      |  -8.40967713781152  |  -5.14829572064257  |
    |     1      |  -8.73195659310182  |   -2.7680086683333  |
    |     1      |  -7.39757567522934  |   -5.4859886576822  |
    |     1      |  -7.31875439049618  |  -3.07666671139964  |
    |     1      |  -6.28257804377125  |  -4.95163379933295  |
    |     1      |  -6.89648773376666  |  -4.70265062279191  |
    |     1      |  -6.60441463655066  |  -6.74908912589265  |
    |     1      |  -6.18017897763298  |   -4.3138626936422  |
    |     1      |  -7.00886675017367  |  -4.42015561015352  |
    |     1      |  -7.33586318666854  |  -6.44810867330437  |
    |     1      |  -6.59611386088473  |  -5.04550354324538  |
    |     1      |  -8.62158710072822  |  -4.29064091029141  |
    |     1      |  -6.29031559279669  |  -3.86667447810372  |
    |     1      |  -8.04380190467639  |  -2.54776583637472  |
    |     1      |  -8.32330346029406  |  -1.43605551283623  |
    |     1      |  -9.56247690113377  |  -1.40623278515704  |
    |     1      |  -6.67578000420508  |  -2.60333192190311  |
    |     1      |  -7.08559030531235  |  -2.54254391069642  |
    |     1      |  -9.78304924433262  |  -1.66724023021163  |
    |     1      |  -6.29266682839611  |  -3.13481658377443  |
    |     1      |  -9.45019268405167  |  -1.98408995381747  |
    |     1      |   -6.9570282366858  |  -2.95501168489224  |
    |     1      |  -7.94363740735857  |  -1.85426192910143  |
    |     1      |  -8.38183062075722  |  -0.99071244289666  |
    |     1      |  -5.78088456568349  |  -4.43288068027835  |
    |     1      |  -5.61285076458605  |  -6.82248345428262  |
    |     1      |  -5.09978727209372  |  -5.83498471222584  |
    |     1      |  -5.68633372694549  |  -4.04597728235925  |
    |     1      |  -5.71947124587347  |  -1.67476947031672  |
    |     1      |  -5.27635207179764  |   -2.4680677300636  |
    |     1      |  -5.72948408114234  |  -2.69785148682904  |
    |     1      |   -5.5024824829318  |  -3.42965639821703  |
    |     1      |  -5.29451921363106  |  -3.94162397549563  |
    |     1      |  -5.10476209926641  |  -3.11914308607538  |
    |     1      |  -5.46293061946655  |  -3.69663436603576  |
    |     1      |  -5.13332996290798  |  -6.66060293869143  |
    |     1      |   -4.3907057560937  |  -6.33599627592414  |
    |     1      |  -4.46413257832831  |  -5.47200646040589  |
    |     1      |  -4.87357620842456  |  -6.31100789472042  |
    |     1      |  -3.90181863396513  |  -5.20756623484547  |
    |     1      |  -4.73847525880601  |  -6.08348819244815  |
    |     1      |  -4.74974100233509  |  -3.83726554635785  |
    |     1      |  -5.33948183773993  |  -8.32312405962642  |
    |     1      |   -4.9163674539497  |  -8.54002596742475  |
    |     1      |  -7.52127250541061  |  -0.465257750109423 |
    |     1      |  -7.04145018804886  |  -0.451612496027543 |
    |     1      |  -9.64087582176592  |  -0.115656335891996 |
    |     1      |  -9.05184511051134  |  0.392023637142042  |
    |     1      |   -7.6094940479889  |  0.103245298426247  |
    |     1      |  -8.32986912612331  |  0.292277797261383  |
    |     1      |  -9.41239379319008  |   1.02342974907878  |
    |     1      |   -5.2884123638684  |  -1.16604869773893  |
    |     1      |  -5.94257287492164  |  -0.585123575564998 |
    |     1      |   -5.6192524431363  |  -0.982091972130393 |
    |     1      |   -5.2957582451849  |  -0.902044712985887 |
    |     1      |  -4.20619644886171  |  -1.78901497823606  |
    |     1      |  -7.80613367343607  |   1.11971051018672  |
    |     1      |  -7.17754788565335  |  0.831913114912767  |
    |     1      |  -3.79505001650893  |  -6.95059119581738  |
    |     1      |  -3.97378933335365  |  -7.44651229001885  |
    |     1      |  -3.24926038889646  |  -5.16841856537779  |
    |     1      |  -4.37454802653498  | -0.0420730235251003 |
    |     1      |  -4.38617225474965  |  -1.02134273900713  |
    |     1      |  -5.86852098622756  |  0.780121679781061  |
    |     1      |   -5.334106048259   |  -0.337809012428767 |
    |     1      |  -4.83532652949697  |  -0.19999668477103  |
    |     1      |  -2.84280797133353  |  -2.41655261833992  |
    |     1      |   -3.3450958288019  |   -7.9449538318184  |
    |     1      |  -2.57837810208014  |   -7.8041677446124  |
    |     1      |  -2.38160564209409  |  -6.08826524395881  |
    |     1      |  -2.42778886688305  |  -5.07906505608888  |
    |     1      |  -2.25335507292922  |  -7.61458046623253  |
    |     1      |  -1.47338601363515  |   -4.7789800701565  |
    |     1      |  -2.61772212228632  |   -9.348080856422   |
    |     1      |  -6.31882555611377  |  0.935916607703975  |
    |     1      |  -5.45952438165412  |   1.05715073228681  |
    |     1      |  -9.15652860848071  |   1.4999929217156   |
    |     1      |  -8.76296128088746  |   2.1137999613368   |
    |     1      |  -9.45603939679267  |   2.0352916196153   |
    |     1      |  -8.55154304697716  |   1.84196265034469  |
    |     1      |  -8.85271198062818  |   2.25723825034557  |
    |     1      |  -8.15093181941236  |   2.30772778964961  |
    |     1      |  -8.98178323124618  |   2.72473292086494  |
    |     1      |  -6.60260227350639  |   2.03586239928187  |
    |     1      |  -3.36659885634044  |  -0.285891923255237 |
    |     1      |  -3.19843129869477  |  -0.895334543145884 |
    |     1      |  -2.69803927871307  |  0.176948350936616  |
    |     1      |  -2.10842919168455  |  -2.34767042675413  |
    |     1      |  -2.26961283584573  |  -2.02879134194403  |
    |     1      |  -7.51514905947966  |   3.07023402912088  |
    |     1      |  -1.79804936600758  |  -7.21527158153023  |
    |     1      |  -1.57933584953627  |  -7.73922007425652  |
    |     1      |  -1.45985176389099  |  -6.84057280274135  |
    |     1      |  -1.77774225910089  |   -3.2238719860203  |
    |     1      |  -1.14314665605461  |   -5.4093134847513  |
    |     1      |  -3.20374889914121  |   1.09063323172304  |
    |     1      |  -3.20331173632448  |  0.602244236786964  |
    |     1      |    -4.51807436278   |   2.15066714778108  |
    |     1      |  -3.20665635783535  |   2.06189257654449  |
    |     1      |  -2.83066687771616  |   1.78199058015924  |
    |     1      |  -4.20395183107068  |   2.63187817886094  |
    |     1      |  -4.59142578513894  |   2.65929589637522  |
    |     1      |  -4.86686860903486  |   2.44415844438791  |
    |     1      |  -0.813276297791525 |  -1.42286654162354  |
    |     1      |  -0.948449583234476 |  -1.91147930543473  |
    |     1      |  -1.07465996922677  |  -3.29774974533252  |
    |     1      |  -0.994720464104191 |  -3.87684144725876  |
    |     1      |  -0.351903676219239 |  -7.73464351786982  |
    |     1      |  -0.468429909305847 |   -7.1392782205433  |
    |     1      |  -0.201163259428537 |  -4.08654533051259  |
    |     1      |  -0.115276821942663 |  -7.33639892997984  |
    |     1      |   0.39117632917649  |  -5.88531089755022  |
    |     1      |  0.705334856503333  |  -5.12118529301192  |
    |     1      |  -5.04815726310395  |   3.29499168009264  |
    |     1      |  -3.89138021221914  |   2.60114946058074  |
    |     1      |  -8.78764020222595  |   4.33311779719457  |
    |     1      |   -5.641866585073   |   4.17952093024716  |
    |     1      |  -4.95134280759438  |   3.84901022252115  |
    |     1      |  -1.69603586741539  |  0.813159230543841  |
    |     1      |  -1.29583147880427  |   1.01913253358525  |
    |     1      |  -1.61652723868216  |  -0.147027238340595 |
    |     1      |  -1.61590369959171  |  0.799951074086106  |
    |     1      |  -0.414671139053382 |   1.08922230596152  |
    |     1      |  -6.32594842292645  |   4.68884703455905  |
    |     1      |  0.246602981466149  |   -8.6126674332715  |
    |     1      |  0.652939989535575  |  -8.09628675603135  |
    |     1      |  -2.91249508639448  |   3.21402896810976  |
    |     1      |  -2.84416721800536  |   3.29575318530935  |
    |     1      |   -4.5082615197209  |   3.65559822584298  |
    |     1      |  -4.34717638154848  |   4.20477387225478  |
    |     1      |  -1.74455196212258  |   3.71657572394077  |
    |     1      |  -2.28071916488964  |   4.02217680310001  |
    |     1      |  -4.95276166822424  |    4.943256990492   |
    |     1      |  0.530182612375441  |  -1.29839535397403  |
    |     1      |   1.35263890556648  |   -0.9451161003416  |
    |     1      |  0.479469145871452  |  0.645953989888518  |
    |     1      |  0.476451874932485  |  0.152693805355902  |
    |     1      |  0.377899618064006  |  -0.946736955524765 |
    |     1      |  0.743589788090247  |  -3.27570388711789  |
    |     1      |  0.354921263807881  |  0.563280047179795  |
    |     1      |   1.52647691384259  |  -8.21857965468363  |
    |     1      |   1.25040294195079  |  -7.82409671592717  |
    |     1      |  0.935720070700963  |  -9.45681583111026  |
    |     1      |   1.24767002242043  |   -8.3407086778156  |
    |     1      |   2.04248554634046  |  -3.32186574736697  |
    |     1      |   2.27912017716054  |  -7.75584315776631  |
    |     1      |   2.61874258174502  |  -5.67264443993226  |
    |     1      |   2.46360438524913  |  -5.10339251491399  |
    |     1      |   2.7888973489352   |  -5.73293558123193  |
    |     1      |  -3.96610977778496  |   5.46526473735704  |
    |     1      |  -6.59997103577478  |   6.37892712670329  |
    |     1      |   -3.0738882967615  |   5.3390446749232   |
    |     1      |  0.265502226662591  |   2.88871821616251  |
    |     1      |   -0.3552143323958  |   3.00026696780709  |
    |     1      |   1.89526876057278  |   1.6089927645442   |
    |     1      |   1.83373646430379  |  0.467395219238194  |
    |     1      |  -6.41633912754075  |   6.9871241026498   |
    |     1      |  -6.95767703324448  |   6.91473181215801  |
    |     1      |   2.80446143485813  |  -6.97256656222631  |
    |     1      |  -1.59565992262012  |   5.04939664856037  |
    |     1      |  -2.62575473292999  |   5.13115170185042  |
    |     1      |  -2.28417562892855  |   5.55342942269213  |
    |     1      |  -3.15919351445474  |   6.39993140306321  |
    |     1      |  0.217321603660157  |   4.37907204701522  |
    |     1      |  -1.68461940795398  |   6.16091568775518  |
    |     1      |  -0.371812484400259 |   4.99593082582389  |
    |     1      |  -0.741417832086523 |   4.93934048104069  |
    |     1      |  -2.44224266728491  |   6.09868204970783  |
    |     1      |  -1.28359582800586  |   5.51822723612107  |
    |     1      |   2.39044021460714  |  -2.76617836801623  |
    |     1      |   2.6516802388484   |  -2.51922619180718  |
    |     1      |   1.74143019679069  |  -0.989194843447391 |
    |     1      |   2.26144590986029  |  -0.37575319892529  |
    |     1      |   2.57904656817161  |   -2.5762806798221  |
    |     1      |   2.70069577391292  |   1.0921575553213   |
    |     1      |   2.05593154395741  |   1.98513857647085  |
    |     1      |   2.9777559419059   |  -2.96397524558193  |
    |     1      |   3.46427696452675  |  -8.40036141611652  |
    |     1      |   3.54751836208045  |  -3.10022171265456  |
    |     1      |   4.71209081574906  |  -7.27491057350995  |
    |     1      |   4.27953158238881  |  -5.52447308577805  |
    |     1      |  -5.25376854243398  |   7.56078737674318  |
    |     1      |  -3.31330377297164  |   6.94184069379319  |
    |     1      |  -6.75761607324594  |   7.23356781398578  |
    |     1      |  -5.71131106266347  |   7.40256357817099  |
    |     1      |  -1.87064242170688  |   7.20106144305368  |
    |     1      |  -1.87012755864771  |   7.27993333585557  |
    |     1      |   2.19031839267831  |   2.75197615509479  |
    |     1      |  0.991456606887029  |   3.4193721755498   |
    |     1      |  0.515416027286751  |   5.24514656292514  |
    |     1      |   2.6829161274633   |   2.95542617000427  |
    |     1      |  0.748390225110757  |   3.96757665740679  |
    |     1      |  0.991360531650185  |   3.20515279341729  |
    |     1      |   0.80737614576117  |   5.1213296293846   |
    |     1      |   1.22632328012321  |   4.36138393094828  |
    |     1      |   2.95972129933523  |   1.36717138409949  |
    |     1      |   3.81279886412099  |  0.826971042355042  |
    |     1      |   3.76077284745908  |  -0.236229035182031 |
    |     1      |  -0.609019869290767 |   7.03669428687389  |
    |     1      |   -4.3115914679652  |   8.49246551212504  |
    |     1      |   1.48190594812944  |   5.99397649801987  |
    |     1      |   1.61782132071341  |   5.56214562410588  |
    |     1      |   1.22641018183269  |   6.6415002181388   |
    |     1      |   1.44932805162357  |   5.45473763507546  |
    |     1      |  -0.830219858712619 |   8.2365631955846   |
    |     1      |  -0.330783431572273 |   7.88353784842581  |
    |     1      |  0.678526512663124  |   7.13463711418893  |
    |     1      |   5.06701549285418  |  -1.99279299564324  |
    |     1      |   4.47805847715496  |  -0.368993445471391 |
    |     1      |   4.70612940131972  |   2.15506268299886  |
    |     1      |   4.98493038815676  |   1.45720642593559  |
    |     1      |   3.13252757914948  |   3.82883450660335  |
    |     1      |   3.22929521707319  |   3.93487430826522  |
    |     1      |   3.46650725857658  |   3.58727350532416  |
    |     1      |   4.54953211105872  |  -8.82700635065651  |
    |     1      |   5.60166986454356  |  -2.93956305502894  |
    |     1      |   5.38993225218259  |  -6.58158049759529  |
    |     1      |    6.225798379735   |   -6.7060116849402  |
    |     1      |   6.25982004043638  |  -6.06218701976453  |
    |     1      |   6.06289634297737  |  -4.24268713884181  |
    |     1      |  -1.46210833055065  |   9.73623859683808  |
    |     1      |  0.983486683565884  |   7.35902272973164  |
    |     1      |   1.71913580583368  |   7.43466171316554  |
    |     1      |   1.80854282891776  |   6.90899744485924  |
    |     1      |   3.02605211410022  |   6.05128344895844  |
    |     1      |   2.85384944307332  |   6.33274446070788  |
    |     1      |   5.69693058528794  |   0.16698499683616  |
    |     1      |   5.16924787087797  | -0.0249290606123065 |
    |     1      |   5.25766014831963  |  0.314951776673528  |
    |     1      |   5.75008538353726  |  -1.27032856981751  |
    |     1      |  0.153150684271544  |   8.8695978274893   |
    |     1      |   2.31280205413364  |   7.28634113319513  |
    |     1      |   2.6748427807702   |   7.19161067027208  |
    |     1      |   2.73953566920922  |   7.38737501082354  |
    |     1      |   3.40497050127246  |   7.51027643564636  |
    |     1      |   3.58825452327181  |   5.87672117905539  |
    |     1      |   3.38506699231689  |   7.23434895148238  |
    |     1      |   2.59695942168914  |   6.95836592324002  |
    |     1      |  0.309873134973399  |   9.57279943841174  |
    |     1      |  0.0704615330651688 |   9.50946975476549  |
    |     1      |   6.9725916241168   |  -0.735864458016987 |
    |     1      |   6.29441900006236  |  -0.704282424740624 |
    |     1      |   6.21819111342458  |  -3.88742747431967  |
    |     1      |   6.17014637969907  |  -3.07587773216696  |
    |     1      |   6.17402555242834  |  -3.53795455467792  |
    |     1      |   7.50245899777043  |  -1.87856749253281  |
    |     1      |   6.56212154615769  |  0.151936966065287  |
    |     1      |   7.17090067321942  |   2.16863075837895  |
    |     1      |   5.40059152776403  |   4.23384053364109  |
    |     1      |   6.88742340397435  |   1.84348943263455  |
    |     1      |   7.14229108632649  |   2.52527433099471  |
    |     1      |   5.72194338576958  |   4.33770242814799  |
    |     1      |   7.06298258018819  |   1.32665043292877  |
    |     1      |   5.18064248151176  |   3.31372851194522  |
    |     1      |   5.00716670183799  |   4.16503539037194  |
    |     1      |    6.780620951569   |   2.09823295106098  |
    |     1      |   7.05472587470651  |   1.24353882448913  |
    |     1      |   4.28784664454304  |   5.39329119743467  |
    |     1      |   4.71393511384443  |   4.9763813125791   |
    |     1      |   7.32439635196905  |   -4.242408431248   |
    |     1      |   7.12560680561029  |  -4.13522491889783  |
    |     1      |   7.2830841957047   |  -4.93409265528158  |
    |     1      |   8.19795409133562  |  -4.67923081232199  |
    |     1      |   3.51634541224518  |   8.88240341976397  |
    |     1      |   3.38587007177336  |   8.3379078555563   |
    |     1      |   3.4466821204157   |   8.2396705347298   |
    |     1      |   5.15830669326629  |   6.82829459050125  |
    |     1      |   4.77705274465357  |   6.2010290735406   |
    |     1      |   7.19891100060144  |  -0.552666089754862 |
    |     1      |   8.14331711183457  |  -0.180568401785832 |
    |     1      |   7.78516333447078  |  -0.163821200916461 |
    |     1      |   5.49445974430743  |   6.8676819637733   |
    |     1      |   5.65772317147708  |   8.15480150196459  |
    |     1      |   5.88118272641729  |   6.57056807380662  |
    |     1      |   5.57292360606274  |   5.6762269584817   |
    |     1      |   9.03192519165199  |  -0.971198031199723 |
    |     1      |   8.31901944164141  |   1.04385704316378  |
    |     1      |   8.10213904739457  |  -2.16905833788638  |
    |     1      |   8.97765118581134  |  -2.13881655230132  |
    |     1      |   9.19346624016458  |  -0.569903194238387 |
    |     1      |   8.49538586032362  |  0.289830989339311  |
    |     1      |   8.58044723914026  |  -0.304584032997761 |
    |     1      |   8.49813308496873  |  -2.94289495467343  |
    |     1      |   8.8115130545625   |  -2.57494027380596  |
    |     1      |   9.56851629520231  |  -0.886411392542726 |
    |     1      |   7.81133921715028  |   1.82518738872613  |
    |     1      |   8.74089283810039  |   2.59950252836547  |
    |     1      |   6.96017444923528  |   4.57285571590664  |
    |     1      |   9.31360566956625  |   2.28798958113789  |
    |     1      |   9.25548584165773  |   2.93263374498702  |
    |     1      |   9.16845455727002  |   1.69505993448899  |
    |     1      |   6.4123281354142   |   4.28930409918041  |
    |     1      |   6.98196878516207  |   5.08948725419561  |
    |     1      |   8.26175050729036  |    4.457774131772   |
    |     1      |   8.66625280988694  |  -4.44359864780847  |
    |     1      |   6.28080577416383  |   7.26276430173906  |
    |     1      |   5.93634832461195  |   7.65253851080897  |
    |     1      |   9.40920831608084  |   0.15981508892021  |
    |     1      |   9.77314010251925  |  0.926589225850343  |
    |     1      |   9.9219424090916   |  -0.284021604007119 |
    +------------+---------------------+---------------------+


![output_27_1](https://user-images.githubusercontent.com/86275885/124321052-04883e80-db4b-11eb-8fca-7a72b1d34f73.png)



     [+] Total Number of Clusters: 3 
    
    +------------+--------------+--------------+
    | Cluster ID | X Coordinate | Y Coordinate |
    +------------+--------------+--------------+
    |     1      |     8.1      |    26.35     |
    |     1      |    10.15     |     27.7     |
    |     1      |     9.75     |     25.5     |
    |     1      |    11.65     |    26.85     |
    |     1      |    12.45     |    27.55     |
    |     1      |     13.3     |    27.85     |
    |     1      |     13.7     |    27.75     |
    |     1      |    14.05     |    26.55     |
    |     1      |    14.15     |     26.9     |
    |     1      |     15.2     |    24.75     |
    |     1      |    16.55     |     27.1     |
    |     1      |    13.25     |     23.5     |
    |     1      |    15.15     |     24.2     |
    |     1      |    13.95     |     22.7     |
    |     1      |     14.4     |    22.65     |
    |     1      |     17.2     |     24.8     |
    |     1      |    17.55     |     25.2     |
    |     1      |     17.0     |    26.85     |
    |     1      |     11.2     |     22.8     |
    |     1      |     12.6     |     23.1     |
    |     1      |    12.15     |    21.45     |
    |     1      |    12.75     |    22.05     |
    |     1      |    13.15     |    21.85     |
    |     1      |    13.75     |     22.0     |
    |     1      |     14.2     |    22.15     |
    |     1      |     14.1     |    21.75     |
    |     1      |    14.05     |     21.4     |
    |     1      |     15.8     |    21.35     |
    |     1      |     17.7     |    24.85     |
    |     1      |    19.15     |    25.35     |
    |     1      |     18.8     |     24.7     |
    |     1      |     12.2     |     20.9     |
    |     1      |     16.6     |    21.15     |
    |     1      |    17.45     |    20.75     |
    |     1      |     18.0     |    20.95     |
    |     1      |     18.0     |     22.3     |
    |     1      |     21.4     |    25.85     |
    |     1      |     18.6     |    22.25     |
    |     1      |    18.25     |     20.2     |
    |     1      |     19.2     |    21.95     |
    |     1      |    19.45     |     22.1     |
    |     1      |     19.9     |    20.35     |
    |     1      |     20.1     |     21.6     |
    |     1      |     20.1     |     20.9     |
    |     1      |    19.45     |    19.05     |
    |     1      |    23.15     |     24.1     |
    |     1      |    19.25     |     18.7     |
    |     1      |     21.3     |     22.3     |
    |     1      |    22.05     |    20.25     |
    |     1      |    20.95     |    18.25     |
    |     1      |     22.9     |    23.65     |
    |     1      |    24.25     |    22.85     |
    |     1      |    22.25     |     18.1     |
    |     1      |    23.15     |    19.05     |
    |     1      |     23.5     |     19.8     |
    |     1      |    23.75     |     20.2     |
    |     1      |     23.0     |     18.0     |
    |     1      |    21.65     |    17.25     |
    |     1      |    21.55     |     16.7     |
    |     1      |     21.6     |     16.3     |
    |     1      |     22.4     |     16.5     |
    |     1      |    23.95     |    17.75     |
    |     1      |    25.15     |     19.8     |
    |     1      |     25.5     |    19.45     |
    |     1      |     21.5     |     15.5     |
    |     1      |     23.5     |     15.2     |
    |     1      |     23.1     |     14.6     |
    |     1      |    24.05     |     14.9     |
    |     1      |     25.9     |    17.55     |
    |     1      |     24.5     |     14.7     |
    |     0      |     3.3      |    15.45     |
    |     0      |     5.25     |     14.2     |
    |     0      |     4.9      |    15.65     |
    |     0      |     5.35     |    15.85     |
    |     0      |     7.2      |     14.5     |
    |     0      |     5.1      |     17.9     |
    |     0      |     7.65     |     16.5     |
    |     0      |     4.6      |    18.25     |
    |     0      |     4.05     |    18.75     |
    |     0      |     3.4      |     19.7     |
    |     0      |     4.4      |    20.05     |
    |     0      |     7.1      |    18.65     |
    |     0      |     2.9      |    21.15     |
    |     0      |     3.1      |    21.85     |
    |     0      |     3.9      |    21.85     |
    |     0      |     5.85     |    20.55     |
    |     0      |     5.5      |     21.8     |
    |     0      |     7.05     |     19.9     |
    |     0      |     6.05     |     22.3     |
    |     0      |     5.2      |     23.4     |
    |     0      |     4.55     |     23.9     |
    |     0      |     6.55     |     21.8     |
    |     0      |     9.2      |     21.1     |
    |     0      |     5.1      |     24.4     |
    |     2      |    14.15     |    17.35     |
    |     2      |     14.3     |     16.8     |
    |     2      |     14.3     |    15.75     |
    |     2      |    14.75     |     15.1     |
    |     2      |    15.35     |     15.5     |
    |     2      |    15.95     |    16.45     |
    |     2      |     16.5     |    17.05     |
    |     2      |    16.65     |     16.1     |
    |     2      |     16.5     |    15.15     |
    |     2      |    16.25     |    14.95     |
    |     2      |     16.0     |    14.25     |
    |     2      |     15.9     |     13.2     |
    |     2      |     17.0     |    15.65     |
    |     2      |     16.9     |    15.35     |
    |     2      |    17.15     |     15.1     |
    |     2      |     17.0     |     14.6     |
    |     2      |    16.85     |     14.3     |
    |     2      |     16.6     |    14.05     |
    |     2      |    17.15     |     16.3     |
    |     2      |    17.35     |    15.45     |
    |     2      |     17.3     |     14.9     |
    |     2      |     17.7     |     15.0     |
    |     2      |     17.1     |     14.0     |
    |     2      |    17.45     |    14.15     |
    |     2      |    17.35     |    17.05     |
    |     2      |     17.8     |     14.2     |
    |     2      |     17.6     |    13.85     |
    |     2      |     17.2     |     13.5     |
    |     2      |    17.25     |    13.15     |
    |     2      |     17.1     |    12.75     |
    |     2      |    16.25     |     12.5     |
    |     2      |    15.15     |    12.05     |
    |     2      |    16.95     |    12.35     |
    |     2      |     16.5     |     12.2     |
    |     2      |    16.05     |     11.9     |
    |     2      |     15.2     |     11.7     |
    |     2      |    16.65     |     10.9     |
    |     2      |     16.7     |     11.4     |
    |     2      |    16.95     |    11.25     |
    |     2      |     17.3     |     11.2     |
    |     2      |    18.05     |     11.9     |
    |     2      |     18.6     |     12.5     |
    |     2      |     18.9     |    12.05     |
    |     2      |     18.7     |    11.25     |
    |     2      |    17.95     |     10.9     |
    |     2      |    17.45     |     10.4     |
    |     2      |     17.6     |    10.15     |
    |     2      |    16.95     |     9.7      |
    |     2      |    16.75     |     9.65     |
    |     2      |     18.4     |    10.05     |
    |     2      |     17.7     |     9.85     |
    |     2      |     17.3     |     9.7      |
    |     2      |     19.1     |     9.55     |
    |     2      |     19.8     |     9.95     |
    |     2      |     19.3     |     9.1      |
    |     2      |     19.4     |     8.85     |
    |     2      |    19.05     |     8.85     |
    |     2      |     17.5     |     8.3      |
    |     2      |    17.55     |     8.1      |
    |     2      |     18.2     |     8.35     |
    |     2      |     18.9     |     8.5      |
    |     2      |    17.85     |     7.55     |
    |     2      |     18.6     |     7.85     |
    |     2      |     18.7     |     7.65     |
    |     2      |    19.35     |     8.2      |
    |     2      |    19.95     |     8.3      |
    |     2      |     20.0     |     8.9      |
    |     2      |     20.3     |     8.9      |
    |     2      |    20.55     |     8.8      |
    |     2      |     21.2     |     8.8      |
    |     2      |     21.4     |     8.8      |
    |     2      |     21.1     |     8.0      |
    |     2      |    18.35     |     6.95     |
    |     2      |    18.65     |     6.9      |
    |     2      |     19.3     |     7.0      |
    |     2      |     19.1     |     6.85     |
    |     2      |    19.15     |     6.65     |
    |     2      |     20.4     |     7.0      |
    |     2      |    21.05     |     7.0      |
    |     2      |    21.85     |     8.5      |
    |     2      |     20.5     |     6.35     |
    |     2      |     20.1     |     6.05     |
    |     2      |     20.9     |     6.6      |
    |     2      |    20.95     |     6.2      |
    |     2      |     21.9     |     8.2      |
    |     2      |     22.3     |     7.7      |
    |     2      |    21.85     |     6.65     |
    |     2      |     22.6     |     6.7      |
    |     2      |    20.95     |     5.55     |
    |     2      |     22.5     |     6.15     |
    |     2      |    20.45     |     5.15     |
    |     2      |     21.3     |     5.05     |
    |     2      |    21.95     |     4.8      |
    |     2      |    22.15     |     5.05     |
    |     2      |    22.45     |     5.3      |
    |     2      |     22.7     |     5.5      |
    |     2      |     23.0     |     5.6      |
    |     2      |    23.65     |     7.2      |
    |     2      |    22.45     |     4.9      |
    |     2      |     23.2     |     5.3      |
    |     2      |    22.95     |     4.75     |
    |     2      |     22.4     |     4.55     |
    |     2      |     24.1     |     7.0      |
    |     2      |    23.45     |     5.95     |
    |     2      |    23.75     |     5.95     |
    |     2      |     23.3     |     4.9      |
    |     2      |    24.45     |     6.15     |
    |     2      |     24.6     |     6.45     |
    |     2      |    24.35     |     5.35     |
    |     2      |     23.8     |     4.75     |
    |     2      |     22.8     |     4.1      |
    |     2      |     22.9     |     4.0      |
    |     2      |    23.25     |     3.85     |
    |     2      |    23.55     |     4.2      |
    |     2      |    23.45     |     3.6      |
    |     2      |     23.8     |     3.65     |
    |     2      |     24.2     |     4.0      |
    |     2      |    24.55     |     4.0      |
    |     2      |     24.7     |     4.3      |
    |     2      |     24.9     |     4.75     |
    |     2      |     25.2     |     6.55     |
    |     2      |     25.3     |     5.75     |
    |     2      |     24.7     |     3.85     |
    |     2      |    25.15     |     4.1      |
    |     2      |    24.95     |     3.35     |
    |     2      |    26.05     |     6.4      |
    |     2      |     25.1     |     3.25     |
    |     2      |     26.4     |     5.7      |
    |     2      |     26.6     |     4.9      |
    |     2      |     26.2     |     4.4      |
    |     2      |     26.0     |     4.25     |
    |     2      |     25.6     |     3.9      |
    |     2      |    25.85     |     3.6      |
    |     2      |    25.45     |     3.15     |
    |     2      |    26.85     |     4.95     |
    |     2      |    26.85     |     4.4      |
    |     2      |    27.15     |     5.95     |
    |     2      |     27.3     |     5.45     |
    |     2      |     27.5     |     5.45     |
    |     2      |    27.55     |     5.1      |
    |     2      |    26.85     |     2.95     |
    |     2      |    27.15     |     3.15     |
    |     2      |     27.2     |     3.0      |
    |     2      |    28.75     |     5.45     |
    |     2      |     28.6     |     5.75     |
    |     2      |    27.95     |     3.25     |
    |     2      |    27.95     |     3.5      |
    |     2      |     28.8     |     4.05     |
    |     2      |     28.8     |     4.7      |
    |     2      |    29.05     |     4.55     |
    |     2      |    29.15     |     4.4      |
    |     2      |     29.2     |     4.0      |
    |     2      |    29.25     |     6.3      |
    |     2      |     29.4     |     4.85     |
    |     2      |     29.5     |     4.7      |
    |     2      |    29.45     |     4.05     |
    |     2      |     29.9     |     4.45     |
    |     2      |     30.0     |     6.55     |
    |     2      |    30.05     |     3.45     |
    |     2      |    29.75     |     3.45     |
    |     2      |    30.75     |     4.45     |
    |     2      |     30.4     |     4.05     |
    |     2      |     30.9     |     5.2      |
    |     2      |    30.65     |     5.85     |
    |     2      |     30.7     |     6.15     |
    |     2      |     30.6     |     3.4      |
    |     2      |     30.8     |     3.95     |
    |     2      |    31.05     |     3.95     |
    |     2      |     31.5     |     6.25     |
    |     2      |    31.65     |     6.55     |
    |     2      |     32.2     |     5.05     |
    |     2      |    32.35     |     4.25     |
    |     2      |     32.0     |     7.0      |
    |     2      |    32.35     |     6.1      |
    |     2      |    32.55     |     5.8      |
    |     2      |     32.9     |     4.15     |
    |     2      |     32.7     |     4.6      |
    |     2      |    32.75     |     4.85     |
    |     2      |     32.6     |     6.95     |
    |     2      |    32.65     |     6.6      |
    |     2      |    32.55     |     6.35     |
    |     2      |    33.35     |     5.65     |
    |     2      |     32.5     |     7.95     |
    |     2      |    33.35     |     7.45     |
    |     2      |     33.6     |     5.25     |
    |     2      |    33.75     |     5.95     |
    |     2      |     33.4     |     6.2      |
    |     2      |     34.1     |     4.6      |
    |     2      |     34.1     |     5.0      |
    |     2      |    34.45     |     5.8      |
    |     2      |    34.35     |     6.8      |
    |     2      |     34.1     |     7.15     |
    |     2      |    34.45     |     7.3      |
    |     2      |    34.35     |     7.75     |
    |     2      |    34.65     |     5.65     |
    |     2      |    34.65     |     6.25     |
    |     2      |     34.7     |     7.2      |
    |     2      |    34.85     |     7.0      |
    |     2      |    34.55     |     7.85     |
    |     2      |    35.25     |     6.25     |
    |     2      |    35.05     |     8.0      |
    |     2      |     35.5     |     8.05     |
    |     2      |     35.8     |     7.1      |
    |     2      |     34.9     |     9.0      |
    |     2      |     36.6     |     6.7      |
    |     2      |    36.75     |     7.25     |
    |     2      |     36.5     |     7.4      |
    |     2      |    35.95     |     7.9      |
    |     2      |     36.1     |     8.1      |
    |     2      |    36.15     |     8.4      |
    |     2      |     35.3     |     9.4      |
    |     2      |     35.9     |     9.35     |
    |     2      |     36.0     |     9.65     |
    |     2      |    35.75     |     10.0     |
    |     2      |     36.7     |     9.15     |
    |     2      |     36.6     |     9.8      |
    |     2      |     37.6     |     7.35     |
    |     2      |     37.9     |     7.65     |
    |     2      |     36.9     |     9.75     |
    |     2      |     36.4     |    10.15     |
    |     2      |     36.3     |     10.7     |
    |     2      |    37.25     |    10.15     |
    |     2      |    38.15     |     9.7      |
    |     2      |     38.4     |     9.45     |
    |     2      |    36.75     |    10.85     |
    |     2      |     37.7     |     10.8     |
    |     2      |    37.45     |    11.15     |
    |     2      |    38.35     |     10.5     |
    |     2      |    37.35     |     11.4     |
    |     2      |     37.0     |    11.75     |
    |     2      |     36.8     |     12.2     |
    |     2      |    37.25     |    12.15     |
    |     2      |    37.65     |    11.95     |
    |     2      |    37.95     |    11.85     |
    |     2      |    37.15     |    12.55     |
    |     2      |     38.6     |    11.75     |
    |     2      |     38.5     |     12.2     |
    |     2      |     39.5     |     11.8     |
    |     2      |     38.0     |    12.95     |
    |     2      |     37.3     |     13.0     |
    |     2      |    38.95     |     12.9     |
    |     2      |     39.2     |    12.35     |
    |     2      |    39.55     |     12.3     |
    |     2      |     37.5     |     13.4     |
    |     2      |     39.0     |     13.2     |
    |     2      |    37.85     |     14.5     |
    |     2      |    38.05     |    14.45     |
    |     2      |    38.35     |    14.35     |
    |     2      |     38.5     |    14.25     |
    |     2      |    39.75     |    12.75     |
    |     2      |     40.2     |     12.8     |
    |     2      |     40.4     |    12.05     |
    |     2      |     38.3     |     14.6     |
    |     2      |    40.45     |     12.5     |
    |     2      |    40.55     |    13.15     |
    |     2      |     39.3     |     14.2     |
    |     2      |    40.45     |     14.5     |
    |     2      |     40.2     |     14.8     |
    |     2      |    38.85     |     15.5     |
    |     2      |    40.65     |     14.9     |
    |     2      |    39.25     |     15.5     |
    |     2      |    39.65     |     16.2     |
    |     2      |     38.3     |     16.5     |
    |     2      |     39.0     |     16.6     |
    |     2      |     40.6     |    15.25     |
    |     2      |     39.9     |     16.2     |
    |     2      |    38.75     |    16.85     |
    |     2      |     41.3     |     15.3     |
    |     2      |    40.95     |     15.7     |
    |     2      |    40.45     |     16.3     |
    |     2      |    41.25     |     16.8     |
    |     2      |     40.7     |    16.45     |
    |     2      |    40.95     |    17.05     |
    |     2      |     39.5     |    16.95     |
    |     2      |     39.9     |    17.05     |
    |     2      |    38.25     |    17.35     |
    |   Noise    |     0.85     |    17.45     |
    |   Noise    |     0.75     |     15.6     |
    |   Noise    |    27.65     |    15.65     |
    +------------+--------------+--------------+



![output_27_3](https://user-images.githubusercontent.com/86275885/124321034-fafed680-db4a-11eb-919b-07f181ee094b.png)



     [+] Total Number of Clusters: 3 
    
    +------------+--------------+--------------+--------------+
    | Cluster ID | X Coordinate | Y Coordinate | Z Coordinate |
    +------------+--------------+--------------+--------------+
    |     2      |    14.15     |    17.35     |     1.0      |
    |     2      |     14.3     |     16.8     |     1.0      |
    |     2      |     14.3     |    15.75     |     1.0      |
    |     2      |    14.75     |     15.1     |     1.0      |
    |     2      |    15.35     |     15.5     |     1.0      |
    |     2      |    15.95     |    16.45     |     1.0      |
    |     2      |     16.5     |    17.05     |     1.0      |
    |     2      |    16.65     |     16.1     |     1.0      |
    |     2      |     16.5     |    15.15     |     1.0      |
    |     2      |    16.25     |    14.95     |     1.0      |
    |     2      |     16.0     |    14.25     |     1.0      |
    |     2      |     15.9     |     13.2     |     1.0      |
    |     2      |     17.0     |    15.65     |     1.0      |
    |     2      |     16.9     |    15.35     |     1.0      |
    |     2      |    17.15     |     15.1     |     1.0      |
    |     2      |     17.0     |     14.6     |     1.0      |
    |     2      |    16.85     |     14.3     |     1.0      |
    |     2      |     16.6     |    14.05     |     1.0      |
    |     2      |    17.15     |     16.3     |     1.0      |
    |     2      |    17.35     |    15.45     |     1.0      |
    |     2      |     17.3     |     14.9     |     1.0      |
    |     2      |     17.7     |     15.0     |     1.0      |
    |     2      |     17.1     |     14.0     |     1.0      |
    |     2      |    17.45     |    14.15     |     1.0      |
    |     2      |    17.35     |    17.05     |     1.0      |
    |     2      |     17.8     |     14.2     |     1.0      |
    |     2      |     17.6     |    13.85     |     1.0      |
    |     2      |     17.2     |     13.5     |     1.0      |
    |     2      |    17.25     |    13.15     |     1.0      |
    |     2      |     17.1     |    12.75     |     1.0      |
    |     2      |    16.25     |     12.5     |     1.0      |
    |     2      |    15.15     |    12.05     |     1.0      |
    |     2      |    16.95     |    12.35     |     1.0      |
    |     2      |     16.5     |     12.2     |     1.0      |
    |     2      |    16.05     |     11.9     |     1.0      |
    |     2      |     15.2     |     11.7     |     1.0      |
    |     2      |    16.65     |     10.9     |     1.0      |
    |     2      |     16.7     |     11.4     |     1.0      |
    |     2      |    16.95     |    11.25     |     1.0      |
    |     2      |     17.3     |     11.2     |     1.0      |
    |     2      |    18.05     |     11.9     |     1.0      |
    |     2      |     18.6     |     12.5     |     1.0      |
    |     2      |     18.9     |    12.05     |     1.0      |
    |     2      |     18.7     |    11.25     |     1.0      |
    |     2      |    17.95     |     10.9     |     1.0      |
    |     2      |    17.45     |     10.4     |     1.0      |
    |     2      |     17.6     |    10.15     |     1.0      |
    |     2      |    16.95     |     9.7      |     1.0      |
    |     2      |    16.75     |     9.65     |     1.0      |
    |     2      |     18.4     |    10.05     |     1.0      |
    |     2      |     17.7     |     9.85     |     1.0      |
    |     2      |     17.3     |     9.7      |     1.0      |
    |     2      |     19.1     |     9.55     |     1.0      |
    |     2      |     19.8     |     9.95     |     1.0      |
    |     2      |     19.3     |     9.1      |     1.0      |
    |     2      |     19.4     |     8.85     |     1.0      |
    |     2      |    19.05     |     8.85     |     1.0      |
    |     2      |     17.5     |     8.3      |     1.0      |
    |     2      |    17.55     |     8.1      |     1.0      |
    |     2      |     18.2     |     8.35     |     1.0      |
    |     2      |     18.9     |     8.5      |     1.0      |
    |     2      |    17.85     |     7.55     |     1.0      |
    |     2      |     18.6     |     7.85     |     1.0      |
    |     2      |     18.7     |     7.65     |     1.0      |
    |     2      |    19.35     |     8.2      |     1.0      |
    |     2      |    19.95     |     8.3      |     1.0      |
    |     2      |     20.0     |     8.9      |     1.0      |
    |     2      |     20.3     |     8.9      |     1.0      |
    |     2      |    20.55     |     8.8      |     1.0      |
    |     2      |     21.2     |     8.8      |     1.0      |
    |     2      |     21.4     |     8.8      |     1.0      |
    |     2      |     21.1     |     8.0      |     1.0      |
    |     2      |    18.35     |     6.95     |     1.0      |
    |     2      |    18.65     |     6.9      |     1.0      |
    |     2      |     19.3     |     7.0      |     1.0      |
    |     2      |     19.1     |     6.85     |     1.0      |
    |     2      |    19.15     |     6.65     |     1.0      |
    |     2      |     20.4     |     7.0      |     1.0      |
    |     2      |    21.05     |     7.0      |     1.0      |
    |     2      |    21.85     |     8.5      |     1.0      |
    |     2      |     20.5     |     6.35     |     1.0      |
    |     2      |     20.1     |     6.05     |     1.0      |
    |     2      |     20.9     |     6.6      |     1.0      |
    |     2      |    20.95     |     6.2      |     1.0      |
    |     2      |     21.9     |     8.2      |     1.0      |
    |     2      |     22.3     |     7.7      |     1.0      |
    |     2      |    21.85     |     6.65     |     1.0      |
    |     2      |     22.6     |     6.7      |     1.0      |
    |     2      |    20.95     |     5.55     |     1.0      |
    |     2      |     22.5     |     6.15     |     1.0      |
    |     2      |    20.45     |     5.15     |     1.0      |
    |     2      |     21.3     |     5.05     |     1.0      |
    |     2      |    21.95     |     4.8      |     1.0      |
    |     2      |    22.15     |     5.05     |     1.0      |
    |     2      |    22.45     |     5.3      |     1.0      |
    |     2      |     22.7     |     5.5      |     1.0      |
    |     2      |     23.0     |     5.6      |     1.0      |
    |     2      |    23.65     |     7.2      |     1.0      |
    |     2      |    22.45     |     4.9      |     1.0      |
    |     2      |     23.2     |     5.3      |     1.0      |
    |     2      |    22.95     |     4.75     |     1.0      |
    |     2      |     22.4     |     4.55     |     1.0      |
    |     2      |     24.1     |     7.0      |     1.0      |
    |     2      |    23.45     |     5.95     |     1.0      |
    |     2      |    23.75     |     5.95     |     1.0      |
    |     2      |     23.3     |     4.9      |     1.0      |
    |     2      |    24.45     |     6.15     |     1.0      |
    |     2      |     24.6     |     6.45     |     1.0      |
    |     2      |    24.35     |     5.35     |     1.0      |
    |     2      |     23.8     |     4.75     |     1.0      |
    |     2      |     22.8     |     4.1      |     1.0      |
    |     2      |     22.9     |     4.0      |     1.0      |
    |     2      |    23.25     |     3.85     |     1.0      |
    |     2      |    23.55     |     4.2      |     1.0      |
    |     2      |    23.45     |     3.6      |     1.0      |
    |     2      |     23.8     |     3.65     |     1.0      |
    |     2      |     24.2     |     4.0      |     1.0      |
    |     2      |    24.55     |     4.0      |     1.0      |
    |     2      |     24.7     |     4.3      |     1.0      |
    |     2      |     24.9     |     4.75     |     1.0      |
    |     2      |     25.2     |     6.55     |     1.0      |
    |     2      |     25.3     |     5.75     |     1.0      |
    |     2      |     24.7     |     3.85     |     1.0      |
    |     2      |    25.15     |     4.1      |     1.0      |
    |     2      |    24.95     |     3.35     |     1.0      |
    |     2      |    26.05     |     6.4      |     1.0      |
    |     2      |     25.1     |     3.25     |     1.0      |
    |     2      |     26.4     |     5.7      |     1.0      |
    |     2      |     26.6     |     4.9      |     1.0      |
    |     2      |     26.2     |     4.4      |     1.0      |
    |     2      |     26.0     |     4.25     |     1.0      |
    |     2      |     25.6     |     3.9      |     1.0      |
    |     2      |    25.85     |     3.6      |     1.0      |
    |     2      |    25.45     |     3.15     |     1.0      |
    |     2      |    26.85     |     4.95     |     1.0      |
    |     2      |    26.85     |     4.4      |     1.0      |
    |     2      |    27.15     |     5.95     |     1.0      |
    |     2      |     27.3     |     5.45     |     1.0      |
    |     2      |     27.5     |     5.45     |     1.0      |
    |     2      |    27.55     |     5.1      |     1.0      |
    |     2      |    26.85     |     2.95     |     1.0      |
    |     2      |    27.15     |     3.15     |     1.0      |
    |     2      |     27.2     |     3.0      |     1.0      |
    |     2      |    28.75     |     5.45     |     1.0      |
    |     2      |     28.6     |     5.75     |     1.0      |
    |     2      |    27.95     |     3.25     |     1.0      |
    |     2      |    27.95     |     3.5      |     1.0      |
    |     2      |     28.8     |     4.05     |     1.0      |
    |     2      |     28.8     |     4.7      |     1.0      |
    |     2      |    29.05     |     4.55     |     1.0      |
    |     2      |    29.15     |     4.4      |     1.0      |
    |     2      |     29.2     |     4.0      |     1.0      |
    |     2      |    29.25     |     6.3      |     1.0      |
    |     2      |     29.4     |     4.85     |     1.0      |
    |     2      |     29.5     |     4.7      |     1.0      |
    |     2      |    29.45     |     4.05     |     1.0      |
    |     2      |     29.9     |     4.45     |     1.0      |
    |     2      |     30.0     |     6.55     |     1.0      |
    |     2      |    30.05     |     3.45     |     1.0      |
    |     2      |    29.75     |     3.45     |     1.0      |
    |     2      |    30.75     |     4.45     |     1.0      |
    |     2      |     30.4     |     4.05     |     1.0      |
    |     2      |     30.9     |     5.2      |     1.0      |
    |     2      |    30.65     |     5.85     |     1.0      |
    |     2      |     30.7     |     6.15     |     1.0      |
    |     2      |     30.6     |     3.4      |     1.0      |
    |     2      |     30.8     |     3.95     |     1.0      |
    |     2      |    31.05     |     3.95     |     1.0      |
    |     2      |     31.5     |     6.25     |     1.0      |
    |     2      |    31.65     |     6.55     |     1.0      |
    |     2      |     32.2     |     5.05     |     1.0      |
    |     2      |    32.35     |     4.25     |     1.0      |
    |     2      |     32.0     |     7.0      |     1.0      |
    |     2      |    32.35     |     6.1      |     1.0      |
    |     2      |    32.55     |     5.8      |     1.0      |
    |     2      |     32.9     |     4.15     |     1.0      |
    |     2      |     32.7     |     4.6      |     1.0      |
    |     2      |    32.75     |     4.85     |     1.0      |
    |     2      |     32.6     |     6.95     |     1.0      |
    |     2      |    32.65     |     6.6      |     1.0      |
    |     2      |    32.55     |     6.35     |     1.0      |
    |     2      |    33.35     |     5.65     |     1.0      |
    |     2      |     32.5     |     7.95     |     1.0      |
    |     2      |    33.35     |     7.45     |     1.0      |
    |     2      |     33.6     |     5.25     |     1.0      |
    |     2      |    33.75     |     5.95     |     1.0      |
    |     2      |     33.4     |     6.2      |     1.0      |
    |     2      |     34.1     |     4.6      |     1.0      |
    |     2      |     34.1     |     5.0      |     1.0      |
    |     2      |    34.45     |     5.8      |     1.0      |
    |     2      |    34.35     |     6.8      |     1.0      |
    |     2      |     34.1     |     7.15     |     1.0      |
    |     2      |    34.45     |     7.3      |     1.0      |
    |     2      |    34.35     |     7.75     |     1.0      |
    |     2      |    34.65     |     5.65     |     1.0      |
    |     2      |    34.65     |     6.25     |     1.0      |
    |     2      |     34.7     |     7.2      |     1.0      |
    |     2      |    34.85     |     7.0      |     1.0      |
    |     2      |    34.55     |     7.85     |     1.0      |
    |     2      |    35.25     |     6.25     |     1.0      |
    |     2      |    35.05     |     8.0      |     1.0      |
    |     2      |     35.5     |     8.05     |     1.0      |
    |     2      |     35.8     |     7.1      |     1.0      |
    |     2      |     34.9     |     9.0      |     1.0      |
    |     2      |     36.6     |     6.7      |     1.0      |
    |     2      |    36.75     |     7.25     |     1.0      |
    |     2      |     36.5     |     7.4      |     1.0      |
    |     2      |    35.95     |     7.9      |     1.0      |
    |     2      |     36.1     |     8.1      |     1.0      |
    |     2      |    36.15     |     8.4      |     1.0      |
    |     2      |     35.3     |     9.4      |     1.0      |
    |     2      |     35.9     |     9.35     |     1.0      |
    |     2      |     36.0     |     9.65     |     1.0      |
    |     2      |    35.75     |     10.0     |     1.0      |
    |     2      |     36.7     |     9.15     |     1.0      |
    |     2      |     36.6     |     9.8      |     1.0      |
    |     2      |     37.6     |     7.35     |     1.0      |
    |     2      |     37.9     |     7.65     |     1.0      |
    |     2      |     36.9     |     9.75     |     1.0      |
    |     2      |     36.4     |    10.15     |     1.0      |
    |     2      |     36.3     |     10.7     |     1.0      |
    |     2      |    37.25     |    10.15     |     1.0      |
    |     2      |    38.15     |     9.7      |     1.0      |
    |     2      |     38.4     |     9.45     |     1.0      |
    |     2      |    36.75     |    10.85     |     1.0      |
    |     2      |     37.7     |     10.8     |     1.0      |
    |     2      |    37.45     |    11.15     |     1.0      |
    |     2      |    38.35     |     10.5     |     1.0      |
    |     2      |    37.35     |     11.4     |     1.0      |
    |     2      |     37.0     |    11.75     |     1.0      |
    |     2      |     36.8     |     12.2     |     1.0      |
    |     2      |    37.25     |    12.15     |     1.0      |
    |     2      |    37.65     |    11.95     |     1.0      |
    |     2      |    37.95     |    11.85     |     1.0      |
    |     2      |    37.15     |    12.55     |     1.0      |
    |     2      |     38.6     |    11.75     |     1.0      |
    |     2      |     38.5     |     12.2     |     1.0      |
    |     2      |     39.5     |     11.8     |     1.0      |
    |     2      |     38.0     |    12.95     |     1.0      |
    |     2      |     37.3     |     13.0     |     1.0      |
    |     2      |    38.95     |     12.9     |     1.0      |
    |     2      |     39.2     |    12.35     |     1.0      |
    |     2      |    39.55     |     12.3     |     1.0      |
    |     2      |     37.5     |     13.4     |     1.0      |
    |     2      |     39.0     |     13.2     |     1.0      |
    |     2      |    37.85     |     14.5     |     1.0      |
    |     2      |    38.05     |    14.45     |     1.0      |
    |     2      |    38.35     |    14.35     |     1.0      |
    |     2      |     38.5     |    14.25     |     1.0      |
    |     2      |    39.75     |    12.75     |     1.0      |
    |     2      |     40.2     |     12.8     |     1.0      |
    |     2      |     40.4     |    12.05     |     1.0      |
    |     2      |     38.3     |     14.6     |     1.0      |
    |     2      |    40.45     |     12.5     |     1.0      |
    |     2      |    40.55     |    13.15     |     1.0      |
    |     2      |     39.3     |     14.2     |     1.0      |
    |     2      |    40.45     |     14.5     |     1.0      |
    |     2      |     40.2     |     14.8     |     1.0      |
    |     2      |    38.85     |     15.5     |     1.0      |
    |     2      |    40.65     |     14.9     |     1.0      |
    |     2      |    39.25     |     15.5     |     1.0      |
    |     2      |    39.65     |     16.2     |     1.0      |
    |     2      |     38.3     |     16.5     |     1.0      |
    |     2      |     39.0     |     16.6     |     1.0      |
    |     2      |     40.6     |    15.25     |     1.0      |
    |     2      |     39.9     |     16.2     |     1.0      |
    |     2      |    38.75     |    16.85     |     1.0      |
    |     2      |     41.3     |     15.3     |     1.0      |
    |     2      |    40.95     |     15.7     |     1.0      |
    |     2      |    40.45     |     16.3     |     1.0      |
    |     2      |    41.25     |     16.8     |     1.0      |
    |     2      |     40.7     |    16.45     |     1.0      |
    |     2      |    40.95     |    17.05     |     1.0      |
    |     2      |     39.5     |    16.95     |     1.0      |
    |     2      |     39.9     |    17.05     |     1.0      |
    |     2      |    38.25     |    17.35     |     1.0      |
    |     0      |     3.3      |    15.45     |     2.0      |
    |     0      |     5.25     |     14.2     |     2.0      |
    |     0      |     4.9      |    15.65     |     2.0      |
    |     0      |     5.35     |    15.85     |     2.0      |
    |     0      |     7.2      |     14.5     |     2.0      |
    |     0      |     5.1      |     17.9     |     2.0      |
    |     0      |     7.65     |     16.5     |     2.0      |
    |     0      |     4.6      |    18.25     |     2.0      |
    |     0      |     4.05     |    18.75     |     2.0      |
    |     0      |     3.4      |     19.7     |     2.0      |
    |     0      |     4.4      |    20.05     |     2.0      |
    |     0      |     7.1      |    18.65     |     2.0      |
    |     0      |     2.9      |    21.15     |     2.0      |
    |     0      |     3.1      |    21.85     |     2.0      |
    |     0      |     3.9      |    21.85     |     2.0      |
    |     0      |     5.85     |    20.55     |     2.0      |
    |     0      |     5.5      |     21.8     |     2.0      |
    |     0      |     7.05     |     19.9     |     2.0      |
    |     0      |     6.05     |     22.3     |     2.0      |
    |     0      |     5.2      |     23.4     |     2.0      |
    |     0      |     4.55     |     23.9     |     2.0      |
    |     0      |     6.55     |     21.8     |     2.0      |
    |     0      |     9.2      |     21.1     |     2.0      |
    |     0      |     5.1      |     24.4     |     2.0      |
    |     1      |     8.1      |    26.35     |     2.0      |
    |     1      |    10.15     |     27.7     |     2.0      |
    |     1      |     9.75     |     25.5     |     2.0      |
    |     1      |    11.65     |    26.85     |     2.0      |
    |     1      |    12.45     |    27.55     |     2.0      |
    |     1      |     13.3     |    27.85     |     2.0      |
    |     1      |     13.7     |    27.75     |     2.0      |
    |     1      |    14.05     |    26.55     |     2.0      |
    |     1      |    14.15     |     26.9     |     2.0      |
    |     1      |     15.2     |    24.75     |     2.0      |
    |     1      |    16.55     |     27.1     |     2.0      |
    |     1      |    13.25     |     23.5     |     2.0      |
    |     1      |    15.15     |     24.2     |     2.0      |
    |     1      |    13.95     |     22.7     |     2.0      |
    |     1      |     14.4     |    22.65     |     2.0      |
    |     1      |     17.2     |     24.8     |     2.0      |
    |     1      |    17.55     |     25.2     |     2.0      |
    |     1      |     17.0     |    26.85     |     2.0      |
    |     1      |     11.2     |     22.8     |     2.0      |
    |     1      |     12.6     |     23.1     |     2.0      |
    |     1      |    12.15     |    21.45     |     2.0      |
    |     1      |    12.75     |    22.05     |     2.0      |
    |     1      |    13.15     |    21.85     |     2.0      |
    |     1      |    13.75     |     22.0     |     2.0      |
    |     1      |     14.2     |    22.15     |     2.0      |
    |     1      |     14.1     |    21.75     |     2.0      |
    |     1      |    14.05     |     21.4     |     2.0      |
    |     1      |     15.8     |    21.35     |     2.0      |
    |     1      |     17.7     |    24.85     |     2.0      |
    |     1      |    19.15     |    25.35     |     2.0      |
    |     1      |     18.8     |     24.7     |     2.0      |
    |     1      |     12.2     |     20.9     |     2.0      |
    |     1      |     16.6     |    21.15     |     2.0      |
    |     1      |    17.45     |    20.75     |     2.0      |
    |     1      |     18.0     |    20.95     |     2.0      |
    |     1      |     18.0     |     22.3     |     2.0      |
    |     1      |     21.4     |    25.85     |     2.0      |
    |     1      |     18.6     |    22.25     |     2.0      |
    |     1      |    18.25     |     20.2     |     2.0      |
    |     1      |     19.2     |    21.95     |     2.0      |
    |     1      |    19.45     |     22.1     |     2.0      |
    |     1      |     19.9     |    20.35     |     2.0      |
    |     1      |     20.1     |     21.6     |     2.0      |
    |     1      |     20.1     |     20.9     |     2.0      |
    |     1      |    19.45     |    19.05     |     2.0      |
    |     1      |    23.15     |     24.1     |     2.0      |
    |     1      |    19.25     |     18.7     |     2.0      |
    |     1      |     21.3     |     22.3     |     2.0      |
    |     1      |    22.05     |    20.25     |     2.0      |
    |     1      |    20.95     |    18.25     |     2.0      |
    |     1      |     22.9     |    23.65     |     2.0      |
    |     1      |    24.25     |    22.85     |     2.0      |
    |     1      |    22.25     |     18.1     |     2.0      |
    |     1      |    23.15     |    19.05     |     2.0      |
    |     1      |     23.5     |     19.8     |     2.0      |
    |     1      |    23.75     |     20.2     |     2.0      |
    |     1      |     23.0     |     18.0     |     2.0      |
    |     1      |    21.65     |    17.25     |     2.0      |
    |     1      |    21.55     |     16.7     |     2.0      |
    |     1      |     21.6     |     16.3     |     2.0      |
    |     1      |     22.4     |     16.5     |     2.0      |
    |     1      |    23.95     |    17.75     |     2.0      |
    |     1      |    25.15     |     19.8     |     2.0      |
    |     1      |     25.5     |    19.45     |     2.0      |
    |     1      |     21.5     |     15.5     |     2.0      |
    |     1      |     23.5     |     15.2     |     2.0      |
    |     1      |     23.1     |     14.6     |     2.0      |
    |     1      |    24.05     |     14.9     |     2.0      |
    |     1      |     25.9     |    17.55     |     2.0      |
    |     1      |     24.5     |     14.7     |     2.0      |
    |   Noise    |     0.85     |    17.45     |     2.0      |
    |   Noise    |     0.75     |     15.6     |     2.0      |
    |   Noise    |    27.65     |    15.65     |     2.0      |
    +------------+--------------+--------------+--------------+



![output_27_5](https://user-images.githubusercontent.com/86275885/124321019-f3d7c880-db4a-11eb-854e-d0bcfe921fce.png)



