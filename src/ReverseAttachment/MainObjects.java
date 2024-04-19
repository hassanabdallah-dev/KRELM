package ReverseAttachment;
import Database.*;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.io.File;
import java.sql.*;

public class MainObjects {

	static DbOperations operations = new DbOperations();
    static String year = "2015";
    
	public static void main(String... args) {
		
		DbConnect.dbname = "graphbipartitereverseattach";
		operations = new DbOperations();
		generateFictiveStatisticsFile();
		

	}
	
	//This method generate the distribution function of connectivity files
	public static void generateFictiveStatisticsFile() {
		ArrayList<String> allProperty = new ArrayList<String>();
		String query = "SELECT distinct propertyCode FROM wikidata_properties t1, degree_distribution t2 where propertyCode LIKE 'P%' and propertyCode = property and year = '"+year+"'";
		ResultSet resultProperties = operations.select(query);
		
		try {
			while(resultProperties.next())
				allProperty.add(resultProperties.getString("propertyCode"));
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		query = "SELECT  distinct t2.propertyCode  FROM properties_objects_fictive_statistics t1, wikidata_properties t2"
				+ " where t1.property_id=t2.id and t1.year = '"+year+"';";
		ResultSet resultPropertiesInDb = operations.select(query);
		ArrayList<String> allPropertiesInDb = new ArrayList<String>();
		try {
			while(resultPropertiesInDb.next())
				allPropertiesInDb.add(resultPropertiesInDb.getString("propertyCode"));
		} catch (SQLException e) {
			;//e.printStackTrace();
		}
		
		int objectNumber, subjectNumber, factNumber1, factNumber2;
		ExecutorService executor = Executors.newFixedThreadPool(5);//creating a pool of 5 threads
		int propertyNumber = 0;
		for(String s : allProperty) {
			
			/*if(s.equals("P106")) {
				propertyNumber++;
				System.out.println(propertyNumber);
				continue;
			}*/
			
			if(allPropertiesInDb.contains(s)) {
				propertyNumber++;
				//System.out.println(propertyNumber);
				System.out.println("algorithm applied for the property "+ s + " ,results exist in the database");
				continue;
			}
			
			objectNumber = getPropertyObjectsNumber(s);
			subjectNumber = getPropertySubjectsNumber(s);
			factNumber1 = getPropertyFactNumber(s);
			factNumber2 = getPropertyFactNumberBySubject(s);
			
			if(factNumber1 == factNumber2) {
				propertyNumber++;
				Runnable graph = new BipartiteGraphObjects(s, factNumber1, subjectNumber, objectNumber, operations, propertyNumber, year);
				executor.execute(graph);
			}
		}
		executor.shutdown(); 

	}
	
	public static int getPropertyObjectsNumber(String property) {
		String query = "SELECT  sum(count) as objNumber FROM degree_distribution where year = '"+year+"' and property = '"+property+"' and type = 'in'";
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
	public static int getPropertySubjectsNumber(String property) {
		String query = "SELECT  sum(count) as sbjNumber FROM degree_distribution where year = '"+year+"' and property = '"+property+"' and type = 'out'";
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
	public static int getPropertyFactNumber(String property) {
		String query = "SELECT  degree, count FROM degree_distribution where year = '"+year+"' and property = '"+property+"' and type = 'out'";
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
	public static int getPropertyFactNumberBySubject(String property) {
		String query = "SELECT  degree, count FROM degree_distribution where year = '"+year+"' and property = '"+property+"' and type = 'in'";
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
