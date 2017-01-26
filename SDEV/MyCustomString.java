package edu.gatech.seclass;
import java.lang.StringBuilder;
import java.util.Map;
import java.util.HashMap;

public class MyCustomString implements MyCustomStringInterface{
	String currentString;
	
	//Static method declared outside and before the Constructor
	public static void print(String string){
		System.out.println(string);
	}
	
	
	//Constructor
	public MyCustomString() {
		this.currentString = null;
	}

	public String getString(){
		return this.currentString;
	}

	public void setString(String string){
		this.currentString = string;
	}

	public int countNumbers(){
		int count = 0;
		boolean isPrevDigit = false;

		String cur = this.currentString;
		if (this.currentString!=null){
			for (int i=0; i < cur.length(); i++){
				if (Character.isDigit(cur.charAt(i))){
					if(!isPrevDigit){
						count++;
						isPrevDigit = true;
					}
				}
				else {
					isPrevDigit = false;
				}
			}
		}
		return count;
		
	}

	public String removeEveryNthCharacter(int n, boolean maintainSpacing){
		String output = "";
		if (n > this.currentString.length()){
			throw new MyIndexOutOfBoundsException();
		}
		 if (n <= 0){
			 throw new IllegalArgumentException(); 
		 }
		if (maintainSpacing){
			char[] charString = this.currentString.toCharArray();
			for (int i=n-1; i<this.currentString.length();i=i+n){
				if (i < this.currentString.length()){
					charString[i] = ' ';
					print(String.valueOf(charString));
				}
			}	
			
			output = String.valueOf(charString);
		}
		
		if (!maintainSpacing){
			StringBuilder sb = new StringBuilder(this.currentString);
			StringBuilder keeper = new StringBuilder("");
			print(keeper.toString());
			for (int i = 0; i < sb.length(); i++){
				if((i+1)%n!=0){
					keeper.append(sb.charAt(i));
					print(keeper.toString());	
				}
				
			}
			output = keeper.toString();				
		}
				
		return output;
	}

	public void convertDigitsToNamesInSubstring(int startPosition, int endPosition){
		if (this.currentString == null){
			throw new NullPointerException();
		}
		if ((startPosition <= endPosition) & (startPosition < 1)){
			throw new IllegalArgumentException();
		}
		if ((startPosition > endPosition) | (endPosition > this.currentString.length())){
			throw new MyIndexOutOfBoundsException();
		}
		Map map = new HashMap();
		map.put(0, "zero");
		map.put(1, "one");
		map.put(2, "two");
		map.put(3, "three");
		map.put(4, "four");
		map.put(5, "five");
		map.put(6, "six");
		map.put(7, "seven");
		map.put(8, "eight");
		map.put(9, "nine");
		int test = Character.getNumericValue(this.currentString.charAt(7));

		//System.out.println(map.get(test));

 		StringBuilder sb = new StringBuilder(this.currentString);
 		
 		StringBuilder output = new StringBuilder("");
 		boolean isPrevDigit = false;
		for (int i = 0;i < sb.length();i++){
			if (Character.isDigit(sb.charAt(i)) & (i>=startPosition-1) & (i<=endPosition-1)){
				String numString = (String) map.get(Character.getNumericValue(sb.charAt(i)));
					
				if (isPrevDigit){
					String dash = "-";
					StringBuilder fullSb = new StringBuilder(dash);
					fullSb.append(numString);
					numString = fullSb.toString();
				}
				output.append(numString);
				//sb.deleteCharAt(i);
				//sb.insert(i,numString);
				//i = i + numString.length();
				isPrevDigit = true;
			}
			
			else{
				output.append(sb.charAt(i));
				isPrevDigit = false;
				
			}		
		}
		this.currentString = output.toString();
		print(output.toString());

	}
			
}
