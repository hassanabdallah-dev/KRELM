package GraphClassModels;

public class Node {

	public int id;
	//After Optimization
	//public ArrayList<Edge> succ = new ArrayList<Edge>();
	public int succ = 0;
	
	public double connectivity = 0;
	
	public Node(int id) {
		this.id = id;
	}
	
}
