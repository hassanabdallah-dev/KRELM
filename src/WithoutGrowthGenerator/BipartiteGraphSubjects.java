package WithoutGrowthGenerator;


import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import Database.DbOperations;
import GraphClassModels.Node;

public class BipartiteGraphSubjects implements Runnable{
		public int initFact = 5;
		
		String property, year;
		int factNumber, subjectsNumber, objectsNumber;
		DbOperations operations;
		int propertyNumber;
		
		
		long startTime, endTime, elapsedTime;
		
		public void run() {

			generateGraph(this.property, this.factNumber, this.subjectsNumber, this.objectsNumber);
			
			int c = insertStagePartSubjectStatistics2Db(this.property, this.operations, 4, this.subjNodes);

			System.out.println(propertyNumber);
		}
		
		//Two Hash Map that countains the nodes in the final graph
		//After Optimization
		public HashMap<Integer, Node> subjNodes = new HashMap<Integer, Node>();
		//public HashMap<Integer, Node> objNodes = new HashMap<Integer, Node>();
		
		//a contructor of the class that launch the construction of the bi-partite graph
		public BipartiteGraphSubjects(String property, int factNumber, int subjectsNumber, int objectsNumber, DbOperations operations, int propertyNumber, String year) {
			this.property = property;
			this.factNumber = factNumber;
			this.subjectsNumber = subjectsNumber;
			this.objectsNumber = objectsNumber;
			this.operations = operations;
			this.propertyNumber = propertyNumber;
			this.year = year;
		}
		
		//Bi-partite graph generator that take the name of the property, the number of fact, number of subject, and number of objects
		public void generateGraph(String p, int fnb, int snb, int onb) {
			
			int s, o;


			int prefSize = factNumber;
			if(factNumber<=5) prefSize = 6;

			int[] peferentialSubject = new int[prefSize];

			
			int indexPrefSubject = 0;

			
			int subjectIndex = 0;

			
			int i = 0, j = snb;
			

			for(i = 0; i < snb ; i++) {
				
				s = subjectIndex++;
				

				this.addSubjNode(s);

				this.addEdge(s);
				

				peferentialSubject[indexPrefSubject++] = s;

			}

			s = -1;
			
			for(j = snb; j < fnb; j++) {

				s = peferentialSubject[(int)(Math.random()*(indexPrefSubject))];	
			
				
				this.addEdge(s);	
				
			}
		}

		
		public void addSubjNode(int n) {
			Node node = new Node(n);
			subjNodes.put(n, node);
		}
		
		//After Optimization
		/*public void addObjNode(int n) {
			Node node = new Node(n);
			objNodes.put(n, node);
		}*/

		public void addEdge(int nS) {
			//Node n = new Node(nS);
			//Node n1 = new Node(nF);
			
			//After Optimization
			if(subjNodes.containsKey(nS) /*&& objNodes.containsKey(nF)*/) {
				//this.getSubjNodes(nS).succ.add(new Edge(n,n1));
				//this.getObjNodes(nF).succ.add(new Edge(n1,n));
				//After Optimization
				//this.getObjNodes(nF).succ++;
				this.getSubjNodes(nS).succ++;
			}
		}
		
		
		public Node getSubjNodes(int n) {
			Node res = subjNodes.get(n);
			return res;
		}
		//After Optimization
		/*public Node getObjNodes(int n) {
			Node res = objNodes.get(n);
			return res;
		}*/
		
		
		public int insertStagePartSubjectStatistics2Db(String property, DbOperations operations, int stage, HashMap<Integer, Node> sbjNodes) {
			int tot = 0;

			HashMap<Integer, Integer> alConn = new HashMap<Integer, Integer>();

			for(Map.Entry<Integer, Node> entry : sbjNodes.entrySet()) {
				//After Optimization
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
			
			String insert = "INSERT INTO properties_subjects_fictive_statistics (property_id, degree, numberOfOccurence, probabilityOfOccuence, type, stage, year) VALUES ";
			
			for(Map.Entry<Integer, Integer> mapentry : alConn.entrySet()) {
				double pk = (double)mapentry.getValue()/(double) tot;
				 insert += "('"+property_id+"', '"+mapentry.getKey()+"', '"+mapentry.getValue()+"', '"+pk+"', '"+"fictiveSubject"+"', '"+stage+"', "+year+"),";
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

		

}
