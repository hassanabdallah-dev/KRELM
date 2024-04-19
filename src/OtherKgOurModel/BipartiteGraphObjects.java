package OtherKgOurModel;


import java.sql.ResultSet;
import java.util.HashMap;
import java.util.Iterator;
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
			startTime = System.currentTimeMillis();
			
			generateGraph(this.property, this.factNumber, this.subjectsNumber, this.objectsNumber);
			
			endTime = System.currentTimeMillis();
			
			elapsedTime = endTime - startTime;
			
			int b = insertStagePartObjectStatistics2Db(this.property, this.operations, kg, this.objNodes);
			//int c = insertStagePartSubjectStatistics2Db(this.property, this.operations, kg, this.subjNodes);
			//int d=  insertPropertyExecutionTime2Db(this.property, this.operations, elapsedTime);
			
			//if(b==1 && c==1 && d==1)
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
			
			int lim = snb+onb+1;
			double ps = 0, po=0;
			Iterator itrs, itro;
			int s, o, indexs, indexo;
			
			//Probability of creating a new subjectr
			double probabilitySubject = (double)snb / (double)fnb;
			//Probability of creating a new object
			double probabilityObject = (double)onb / (double)fnb;
			
			//Convert probabilities to % format
			ps = (double) (probabilitySubject*100);
			po = (double) (probabilityObject*100);

			//Allows to represent the preferential attachment. There are, in each list, the duplicated nodes according to the links
			int prefSize = factNumber;
			if(factNumber<=5) prefSize = 6;
			//int[] peferentialSubject = new int[prefSize];
			int[] peferentialObject = new int[prefSize];
			
			int indexPrefSubject = 0;
			int indexPrefObject = 0;
			
			int subjectIndex = 0;
			int objectIndex = snb;
			
			int i = 0, j = this.initFact;
			
			//Initialize the number of fact already present in the bipartite graph
			for(i = 0; i < this.initFact ; i++) {
				
				//Randomly take a subject and an object from the temporary lists
				s = subjectIndex++;
				o = objectIndex++;
				
				//Add the subject and object and link them in the final graph
				//this.addSubjNode(s);
				this.addObjNode(o);
				this.addEdge(s, o);
				
				//add the subject and object to the preferential lists to represent the preferential attachment
				//peferentialSubject[indexPrefSubject++] = s;
				peferentialObject[indexPrefObject++] = o;

			}

			//Body of the algo begin here
			//int partLength = (int) Math.ceil(fnb/4);
			s = -1;
			o = -1;
			
			for(j = this.initFact; j < fnb; j++) {
				//randomly take two numbers between 1 and 100
				double pForNewSubj = (double)(Math.random()*100);
				double pForNewObj = (double)(Math.random()*100);

				//If this condition is true, so a new object will be added
				if(pForNewObj <= po) {

					if(objectIndex < snb + onb) 
						o = objectIndex++;
					else 
						o = lim++;
					
					//Add the object to the final graph
					this.addObjNode(o);
				}
				else 
					//take an object using preferential attachment
					o = peferentialObject[(int)(Math.random()*(indexPrefObject))];	
				

				if(pForNewSubj <= ps) {

					if(subjectIndex < snb) 	
						s = subjectIndex++;
						
					
					else 
						s = lim++;
					
					
					//Add the subject to the final graph
					//this.addSubjNode(s);
				}
				else 
					//take an subject using preferential attachment
					;//s = peferentialSubject[(int)(Math.random()*(indexPrefSubject- 1))];					
				

				//add a link between the subject and the object to the final graph
				this.addEdge(s, o);
				
				
				//add the subject and object to the preferential lists to represent the preferential attachment
				//peferentialSubject[indexPrefSubject++] = s;
				peferentialObject[indexPrefObject++] = o;
				//int b,c;
				
				/*if(j==partLength) {
					b = insertStagePartObjectStatistics2Db(this.property, this.operations, 1, this.objNodes);
					c = insertStagePartSubjectStatistics2Db(this.property, this.operations, 1, this.subjNodes);
				}
				else if(j==partLength*2) {
					b = insertStagePartObjectStatistics2Db(this.property, this.operations, 2, this.objNodes);
					c = insertStagePartSubjectStatistics2Db(this.property, this.operations, 2, this.subjNodes);
				}
				else if(j==partLength*3) {
					b = insertStagePartObjectStatistics2Db(this.property, this.operations, 3, this.objNodes);
					c = insertStagePartSubjectStatistics2Db(this.property, this.operations, 3, this.subjNodes);
				}*/
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


		public void addEdge(int nS, int nF) {
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
