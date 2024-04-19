package WithoutGrowthGenerator;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import Database.DbOperations;
import GraphClassModels.Node;

public class BipartiteGraphObjects implements Runnable{
		public int initFact = 5;
		
		String property, year;
		int factNumber, subjectsNumber, objectsNumber;
		DbOperations operations;
		int propertyNumber;
		
		
		long startTime, endTime, elapsedTime;
		
		public void run() {
			generateGraph(this.property, this.factNumber, this.subjectsNumber, this.objectsNumber);
			
			int b = insertStagePartObjectStatistics2Db(this.property, this.operations, 4, this.objNodes);

			System.out.println(propertyNumber);
		}
		

		public HashMap<Integer, Node> objNodes = new HashMap<Integer, Node>();
		

		public BipartiteGraphObjects(String property, int factNumber, int subjectsNumber, int objectsNumber, DbOperations operations, int propertyNumber, String year) {
			this.property = property;
			this.factNumber = factNumber;
			this.subjectsNumber = subjectsNumber;
			this.objectsNumber = objectsNumber;
			this.operations = operations;
			this.propertyNumber = propertyNumber;
			this.year = year;
		}
		

		public void generateGraph(String p, int fnb, int snb, int onb) {
			
			int  o;

			int prefSize = factNumber;
			if(factNumber <= 5) prefSize = 6;
			int[] peferentialObject = new int[prefSize];
			
			int indexPrefObject = 0;
			
			int objectIndex = snb;
			
			int i = 0, j = this.initFact;
			
			for(i=0; i < onb; i++) {
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

		//After Optimization
		/*public void addSubjNode(int n) {
			Node node = new Node(n);
			subjNodes.put(n, node);
		}*/

		public void addObjNode(int n) {
			Node node = new Node(n);
			objNodes.put(n, node);
		}


		public void addEdge(int nF) {
			//Node n = new Node(nS);
			//Node n1 = new Node(nF);
			
			//After Optimization
			if(/*subjNodes.containsKey(nS) && */objNodes.containsKey(nF)) {
				//this.getSubjNodes(nS).succ.add(new Edge(n,n1));
				//this.getObjNodes(nF).succ.add(new Edge(n1,n));
				this.getObjNodes(nF).succ++;
			}
		}
		
		//After Optimization
		/*public Node getSubjNodes(int n) {
			Node res = subjNodes.get(n);
			return res;
		}*/

		public Node getObjNodes(int n) {
			Node res = objNodes.get(n);
			return res;
		}
		
		
		public int insertStagePartObjectStatistics2Db(String property, DbOperations operations, int stage, HashMap<Integer, Node> objNodes) {
			int tot = 0;

			HashMap<Integer, Integer> alConn = new HashMap<Integer, Integer>();

			for(Map.Entry<Integer, Node> entry : objNodes.entrySet()) {
				//After Optimization
				//int conn = entry.getValue().succ.size();
				int conn = entry.getValue().succ;

				if(!alConn.containsKey(conn)) alConn.put(conn, 1);
				else {
					int nbWithThisConn = alConn.get(conn);
					nbWithThisConn++;
					alConn.put(conn, nbWithThisConn);
				}
			}

			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				tot += mapentry.getValue();
			}
			
			String query = "SELECT id FROM `wikidata_properties` where  propertyCode = '"+property+"'";
			ResultSet resultObjects = operations.select(query);
			int property_id=-1;
			
			try {
				while(resultObjects.next())
					property_id = resultObjects.getInt("id");
			} catch (Exception e) {
				operations = new DbOperations();
				query = "SELECT id FROM `wikidata_properties` where  propertyCode = '"+property+"'";
				resultObjects = operations.select(query);
				try {
					while(resultObjects.next())
						property_id = resultObjects.getInt("id");
				} catch (SQLException e1) {
					e1.printStackTrace();
				}
			}
			
			String insert = "INSERT INTO properties_objects_fictive_statistics (property_id, degree, numberOfOccurence, probabilityOfOccuence, type, stage, year) VALUES ";
			double sumOfprob = 0;
			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				double pk = (double)mapentry.getValue()/(double) tot;
				sumOfprob += pk;
				insert += "('"+property_id+"', '"+mapentry.getKey()+"', '"+mapentry.getValue()+"', '"+pk+"', '"+"fictiveObject"+"', '"+stage+"', '"+year+"'),";
			}
			
			//if(sumOfprob < 0.99 || sumOfprob > 1.001)
			//	System.out.print(sumOfprob);
				
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
		


}
