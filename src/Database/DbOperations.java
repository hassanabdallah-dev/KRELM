package Database;
import java.sql.*;


public class DbOperations {
	public DbConnect Db;
	public DbOperations() {
		 this.Db = new DbConnect();
	}
	
	public ResultSet select(String query) {
		try {	
			PreparedStatement preparedStatement=DbConnect.connection.prepareStatement(query);
	        //Creating Java ResultSet object
	        ResultSet resultSet=preparedStatement.executeQuery();
	       
	        return resultSet;
		}catch(SQLException e) {
			System.out.println("Error while retrieving data from database");
			return null;
		}
	}
	public void insert(String query) {
		try {	
			PreparedStatement preparedStatement=DbConnect.connection.prepareStatement(query);

	        preparedStatement.executeUpdate();
	       

		}catch(SQLException e) {
			System.out.println("Error while inserting data to the database");

		}
	}
	public void delete(String query) {
		PreparedStatement preparedStatement;
		try {
			preparedStatement = DbConnect.connection.prepareStatement(query);
			preparedStatement.executeUpdate();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

        
	}
}
