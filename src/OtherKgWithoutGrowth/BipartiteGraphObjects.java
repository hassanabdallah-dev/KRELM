package OtherKgWithoutGrowth;

import java.sql.ResultSet;
import java.util.HashMap;
import java.util.Map;
import Database.DbOperations;
import GraphClassModels.Node;

public class BipartiteGraphObjects implements Runnable{
		public int initFact = 5;
		
		String property;
		String kg;
		int factNumber, subjectsNumber, objectsNumber;
		DbOperations operations;
		int propertyNumber;
		
		
		long startTime, endTime, elapsedTime;
		
		public void run() {
			generateGraph(this.property, this.factNumber, this.subjectsNumber, this.objectsNumber);
			
			int b = insertStagePartObjectStatistics2Db(this.property, this.operations, kg, this.objNodes);

			 System.out.println(propertyNumber);
		}
		
		//Two Hash Map that countains the nodes in the final graph
		//public HashMap<Integer, Node> subjNodes = new HashMap<Integer, Node>();
		public HashMap<Integer, Node> objNodes = new HashMap<Integer, Node>();
		
		//a contructor of the class that launch the construction of the bi-partite graph
		public BipartiteGraphObjects(String property, int factNumber, int subjectsNumber, int objectsNumber, DbOperations operations, int propertyNumber, String kg) {
			this.property = property;
			this.factNumber = factNumber;
			this.subjectsNumber = subjectsNumber;
			this.objectsNumber = objectsNumber;
			this.operations = operations;
			this.propertyNumber = propertyNumber;
			this.kg = kg;
		}
		
		//Bi-partite graph generator that take the name of the property, the number of fact, number of subject, and number of objects
		public void generateGraph(String p, int fnb, int snb, int onb) {
			
			int o;
			
			int prefSize = factNumber;
			if(factNumber<=5) prefSize = 6;

			int[] peferentialObject = new int[prefSize];
			

			int indexPrefObject = 0;
			
			int objectIndex = snb;
			
			int i = 0, j = onb;
			
			/*o = objectIndex++;
			this.addObjNode(o);
			this.addEdge(o);
			peferentialObject[indexPrefObject++] = o;*/
			
			//Initialize the number of fact already present in the bipartite graph
			for(i = 0; i < onb ; i++) {
				
				o = objectIndex++;
				

				this.addObjNode(o);
				this.addEdge(o);

				peferentialObject[indexPrefObject++] = o;

			}


			o = -1;
			
			for(j = onb; j < fnb; j++) {

				o = peferentialObject[(int)(Math.random()*(indexPrefObject))];	
				

				this.addEdge(o);
				
				
				peferentialObject[indexPrefObject++] = o;

			}
		}

	
		public void addSubjNode(int n) {
			Node node = new Node(n);
			//subjNodes.put(n, node);
		}

		public void addObjNode(int n) {
			Node node = new Node(n);
			objNodes.put(n, node);
		}


		public void addEdge(int nF) {
			//Node n = new Node(nS);
			//Node n1 = new Node(nF);

			if(/*subjNodes.containsKey(nS) &&*/ objNodes.containsKey(nF)) {
				//this.getSubjNodes(nS).succ.add(new Edge(n,n1));
				//this.getObjNodes(nF).succ.add(new Edge(n1,n));
				this.getObjNodes(nF).succ++;
			}
		}
		
		/*public Node getSubjNodes(int n) {
			Node res = subjNodes.get(n);
			return res;
		}*/

		public Node getObjNodes(int n) {
			Node res = objNodes.get(n);
			return res;
		}
		
		
		public int insertStagePartObjectStatistics2Db(String property, DbOperations operations, String kg, HashMap<Integer, Node> objNodes) {
			int tot = 0;

			HashMap<Integer, Integer> alConn = new HashMap<Integer, Integer>();

			for(Map.Entry<Integer, Node> entry : objNodes.entrySet()) {
				//int conn = entry.getValue().succ.size();
				int conn = entry.getValue().succ;
				if(!alConn.containsKey(conn)) alConn.put(conn, 1);
				else {
					int nbWithThisConn = alConn.get(conn);
					nbWithThisConn ++;
					alConn.put(conn, nbWithThisConn);
				}
			}

			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				tot += mapentry.getValue();
			}
			
			String insert = "INSERT INTO properties_objects_fictive_statistics (property, degree, numberOfOccurence, probabilityOfOccuence, kg) VALUES ";
			
			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				double pk = (double)mapentry.getValue()/(double) tot;
				 insert += "('"+property+"', '"+mapentry.getKey()+"', '"+mapentry.getValue()+"', '"+pk+"', '"+kg+"'),";

			}
			insert = insert.substring(0, insert.length() - 1);
			insert += ";";
			
			if(!alConn.isEmpty()) {
				operations.insert(insert);
				return 1;
			}
			else {
				return 0;
			}
			
		}
		
		
		public int insertStagePartSubjectStatistics2Db(String property, DbOperations operations, String kg, HashMap<Integer, Node> sbjNodes) {
			int tot = 0;

			HashMap<Integer, Integer> alConn = new HashMap<Integer, Integer>();

			for(Map.Entry<Integer, Node> entry : sbjNodes.entrySet()) {
				//int conn = entry.getValue().succ.size();
				int conn = entry.getValue().succ;

				if(!alConn.containsKey(conn)) alConn.put(conn, 1);
				else {
					int nbWithThisConn = alConn.get(conn);
					nbWithThisConn ++;
					alConn.put(conn, nbWithThisConn);
				}
			}

			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				tot += mapentry.getValue();
			}
			
			String insert = "INSERT INTO properties_subjects_fictive_statistics (property, degree, numberOfOccurence, probabilityOfOccuence, kg) VALUES ";
			
			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				double pk = (double)mapentry.getValue()/(double) tot;
				 insert += "('"+property+"', '"+mapentry.getKey()+"', '"+mapentry.getValue()+"', '"+pk+"', '"+kg+"'),";

			}
			insert = insert.substring(0, insert.length() - 1);
			insert += ";";
			
			if(!alConn.isEmpty()) {
				operations.insert(insert);
				return 1;
			}
			else {
				return 0;
			}
			
		}

		
		public int insertPropertyExecutionTime2Db(String property, DbOperations operations, long elapsedTime) {
			String query = "SELECT property FROM `properties_objects_characteristics` where  property = '"+property+"'";
			ResultSet resultObjects = operations.select(query);
			String checkProperty=null;
			
			try {
				while(resultObjects.next())
					checkProperty = resultObjects.getString("property");
			} catch (Exception e) {;}
			
			if(checkProperty==null)
			{
				String insert = "INSERT INTO properties_objects_characteristics (property, executionTime) VALUES ('"+property+"', "+elapsedTime+")";
				operations.insert(insert);
				return 1;
			}else {
				String update = "UPDATE properties_objects_characteristics SET executionTime = "+elapsedTime+" WHERE property = '"+property+"'";
				operations.insert(update);
				return 1;
			}
		}
}
