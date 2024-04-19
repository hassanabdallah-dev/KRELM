package GraphClassModels;

public class wikiDataSnapshot {
	
	public int objectNumber;
	public int subjectNumber;
	public int factNumber1;
	public int factNumber2;
	public String property;
	public String year;
	
	public wikiDataSnapshot(String property, String year, int objectNumber, int subjectNumber, int factNumber1, int factNumber2) {
		this.property = property;
		this.year = year;
		this.objectNumber = objectNumber;
		this.subjectNumber = subjectNumber;
		this.factNumber1 = factNumber1;
		this.factNumber2 = factNumber2;
	}
	
	public double calculateObjectProbability() {
		try{
			return ((double)objectNumber/factNumber1)*100;
		}
		catch(Exception e) {
			return 0;
		}
		
	}
	
	public double calculateSubjectProbability() {
		try{	
				return ((double)subjectNumber/factNumber1)*100;
		}
		catch(Exception e) {
			return 0;
		}
	}
}
