import csv
import prettytable
import scipy.spatial as scp
import matplotlib.pyplot as matp



class Plot:

	def __init__(self, dimension):
		self.colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
		self.dimension = dimension
		self.ax = None


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


	def import_dataset(self):
		with open(self.filename, "rt") as dataset_csvfile:
			dataset_reader = csv.reader(dataset_csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
			self.dataset = list(dataset_reader)


	def region_query(self, s_point):
		r = []
		for d_point in self.dataset:
			if s_point != d_point:
				if scp.distance.euclidean(d_point[:self.dimension], s_point[:self.dimension]) <= self.eps:
					r.append(d_point)
		return r


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


def main():
	print("\n" + "="*70)
	print(" DBSCAN Algorithm")
	print("="*70 + "\n")
	Dbscan(filename="annulus.csv", dimension=2).start()
	Dbscan(filename="jain.csv", dimension=2).start()
	Dbscan(filename="jain.csv", dimension=3).start()


main()

