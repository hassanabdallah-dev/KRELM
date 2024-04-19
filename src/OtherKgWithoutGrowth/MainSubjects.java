package OtherKgWithoutGrowth;
import Database.*;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.io.File;
import java.sql.*;

public class MainSubjects {

	static DbOperations operations = new DbOperations();
    
    
	public static void main(String... args) {
		
		DbConnect.dbname = "graphbipartiteallkgwithoutgrowth";
		operations = new DbOperations();
		generateFictiveStatisticsFile();
		
		//double[] p1 = new double[] {0.25, 0.33, 0.23, 0.19};
		//double[] p2 = new double[] {0.21, 0.21, 0.32, 0.26};
		
		
		
		//double result = klDivergence(p2, p1);
		
		//System.out.println(result);
	}
	
	//This method generate the distribution function of connectivity files
	public static void generateFictiveStatisticsFile() {
		
		ArrayList<String> allKgs = new ArrayList<String>();
		
		allKgs.add("YAGO4");
		allKgs.add("DBPEDIA");
		allKgs.add("DBNARY");
		
		int propertyNumber = 0;
		ExecutorService executor = Executors.newFixedThreadPool(1);//creating a pool of 5 threads
		
		String query;
		
		for(String kg : allKgs)
		{	
			//if(kg.equals("DBPEDIA") || kg.equals("BNF")) 
				//continue;
			
			query = "SELECT  distinct property FROM degree_distribution"
					+ " where kg = '"+ kg +"';";
			
			ResultSet resultPropertiesInDb = operations.select(query);
			ArrayList<String> allProperty = new ArrayList<String>();
			try {
				while(resultPropertiesInDb.next())
					allProperty.add(resultPropertiesInDb.getString("property"));
			} catch (SQLException e) {
				;//e.printStackTrace();
			}
			
			query = "SELECT  distinct property FROM properties_subjects_fictive_statistics"
					+ " where kg = '"+ kg +"';";
			
			 resultPropertiesInDb = operations.select(query);
			ArrayList<String> allPropertiesInDb = new ArrayList<String>();
			try {
				while(resultPropertiesInDb.next())
				{
					String temp = resultPropertiesInDb.getString("property");
					if(temp.contains("'"))
						temp= temp.replace("'", "\\'");
					allPropertiesInDb.add(temp);
				}
			} catch (SQLException e) {
				;//e.printStackTrace();
			}
			
			
			int objectNumber, subjectNumber, factNumber1, factNumber2;
			
			
			for(String s : allProperty) {
				
				
				
				if(s.equals("all")) 
					continue;
				
				if(s.contains("'"))
					s= s.replace("'", "\\'");
				
				/*if(kg.equals("DBNARY") == false || s.equals("22-rdf-syntax-ns#type") == false) {
					continue;
				}*/
				
				if(allPropertiesInDb.contains(s)) {
					propertyNumber++;
					//System.out.println(propertyNumber);
					System.out.println("algorithm applied for the property "+ s + " ,results exist in the database");
					continue;
				}
				
				objectNumber = getPropertyObjectsNumber(s, kg);
				subjectNumber = getPropertySubjectsNumber(s, kg);
				factNumber1 = getPropertyFactNumber(s, kg);
				factNumber2 = getPropertyFactNumberBySubject(s, kg);
				
				//if(factNumber1 == factNumber2) {
					propertyNumber++;
					

					
					//String insert = "INSERT INTO kgs_properties (property, kg, factNumber, objectsNumber, sujectsNumber) VALUES ('"+s+"', '"+kg+"', '"+factNumber1+"', '"+objectNumber+"', '"+subjectNumber+"')";
					//operations.insert(insert);

					Runnable graph = new BipartiteGraphSubjects(s, factNumber1, subjectNumber, objectNumber, operations, propertyNumber, kg);
					executor.execute(graph);
				//}
				//else {
				//	System.out.print("I am here");
				//}
			}
			
			
			
		}
		executor.shutdown(); 
	}
	
	public static int getPropertyObjectsNumber(String property, String kg) {
		String query = "SELECT  sum(count) as objNumber FROM degree_distribution where kg = '"+kg+"' and property = '"+property+"' and type = 'IN'";
		ResultSet resultObjects = operations.select(query);
		int objNumber=0;
		
		try {
			while(resultObjects.next())
				objNumber = resultObjects.getInt("objNumber");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return objNumber;
	}
	public static int getPropertySubjectsNumber(String property, String kg) {
		String query = "SELECT  sum(count) as sbjNumber FROM degree_distribution where kg = '"+kg+"' and property = '"+property+"' and type = 'OUT'";
		ResultSet resultSubjects = operations.select(query);
		int sbjNumber=0;
		
		try {
			while(resultSubjects.next())
				sbjNumber = resultSubjects.getInt("sbjNumber");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return sbjNumber;
	}
	public static int getPropertyFactNumber(String property, String kg) {
		String query = "SELECT  degree, count FROM degree_distribution where kg = '"+kg+"' and property = '"+property+"' and type = 'OUT'";
		ResultSet resultFacts = operations.select(query);
		int fctNumber=0, degree=0, count=0;
		
		try {
			while(resultFacts.next()) {
				degree = resultFacts.getInt("degree");
				count = resultFacts.getInt("count");
				fctNumber += degree*count;
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return fctNumber;
	}
	public static int getPropertyFactNumberBySubject(String property, String kg) {
		String query = "SELECT  degree, count FROM degree_distribution where kg = '"+kg+"' and property = '"+property+"' and type = 'IN'";
		ResultSet resultFacts = operations.select(query);
		int fctNumber=0, degree=0, count=0;
		
		try {
			while(resultFacts.next()) {
				degree = resultFacts.getInt("degree");
				count = resultFacts.getInt("count");
				fctNumber += degree*count;
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return fctNumber;
	}
	
	public static ArrayList<String> getPropertyInFolder(){
		
		File directoryPath = new File("statisticsFiles");
		
	    ArrayList<String> allProperties = new ArrayList<String>();  
	    String contents[] = directoryPath.list();
	    
	    for(int i=0; i<contents.length; i++) 
	    	  allProperties.add(contents[i].split("_")[0]);
	       
		
		return allProperties;
	}
	

	
	
}
