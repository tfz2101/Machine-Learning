package edu.gatech.seclass;

public class MyTester {

	public MyTester() {
		// TODO Auto-generated constructor stub
	}

	public static void main(String[] args) {
		MyCustomString string = new MyCustomString();
		string.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
		//System.out.println(string.countNumbers());
		//System.out.println(string.removeEveryNthCharacter(3, false));
		string.convertDigitsToNamesInSubstring(0,8);
		
	}

}
