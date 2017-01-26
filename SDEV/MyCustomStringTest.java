package edu.gatech.seclass;

import org.junit.After;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

public class MyCustomStringTest {

    private MyCustomStringInterface mycustomstring;

    @Before
    public void setUp() {
        mycustomstring = new MyCustomString();
    }

    @After
    public void tearDown() {
        mycustomstring = null;
    }

    @Test
    public void testCountNumbers1() {
        mycustomstring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        assertEquals(7, mycustomstring.countNumbers());
    }

    @Test
    public void testCountNumbers2() {
        //Test if its a empty string, it returns 0
        mycustomstring.setString("");
        assertEquals(0, mycustomstring.countNumbers());
    }

    @Test
    public void testCountNumbers3() {
        //Test if its unset string, it returns 0
        assertEquals(0, mycustomstring.countNumbers());
    }

    @Test
    public void testCountNumbers4() {
        //Test if there are no numbers in the string, it returns 0
        mycustomstring.setString("There are no numbers in this sentence");
        assertEquals(0, mycustomstring.countNumbers());

    }

    @Test
    public void testCountNumbers5() {
        //Test if the string consists of all numbers, it returns 1
        mycustomstring.setString("1234567");
        assertEquals(1	, mycustomstring.countNumbers());
    }
    
    
    @Test
    public void testCountNumbers6() {
        //Test if the string consists if numbers separated by spaces, it returns the number of single digits
    	mycustomstring.setString("1 2 3 4 5 6 7");
    	assertEquals(7, mycustomstring.countNumbers());
    }

    
    @Test
    public void testremoveEveryNthCharacter1() {
        mycustomstring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        assertEquals("I' bttr uts0e 16tsinths trn6 rgh?", mycustomstring.removeEveryNthCharacter(3, false));
    }
    
   
    @Test
    public void testremoveEveryNthCharacter2() {
        mycustomstring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        assertEquals("I'  b tt r  ut s0 e  16 ts in th s  tr n6  r gh ?", mycustomstring.removeEveryNthCharacter(3, true));
    }
    
  
    @Test(expected = MyIndexOutOfBoundsException.class)
    //Test for MyIndexOutOfBoundsException if n > string's length
    public void testremoveEveryNthCharacter3() {
    	//throw new MyIndexOutOfBoundsException();

    	try {
    		mycustomstring.setString("Short");
    		mycustomstring.removeEveryNthCharacter(7, false);
    		fail();
    	}catch (Exception e){	
    		if (MyIndexOutOfBoundsException.class.isInstance(e)){
    			throw new MyIndexOutOfBoundsException();
    		}
    	}
    	
    }
   
    

    @Test(expected = IllegalArgumentException.class)
    public void testremoveEveryNthCharacter4() {
    	try {
    		mycustomstring.setString("Short");
    		mycustomstring.removeEveryNthCharacter(0, false);
    		fail();
    	}catch (Exception e){	
    		if (IllegalArgumentException.class.isInstance(e)){
    			throw new IllegalArgumentException();
    		}
    	}
    }
    
    
    @Test
    public void testremoveEveryNthCharacter5() {
    	//Test if input string is only one letter, and n = 1. Should return an empty string.
    	mycustomstring.setString("i");
        assertEquals("", mycustomstring.removeEveryNthCharacter(1, false));
    }
    
    
    @Test
    public void testremoveEveryNthCharacter6() {
    	//Test if input string is only one letter, and n = 1. Should return 1 empty space.
    	mycustomstring.setString("i");
        assertEquals(" ", mycustomstring.removeEveryNthCharacter(1, true));
    }

    
    @Test
    public void testremoveEveryNthCharacter7() {
       	//Test if n = 1, empty string is returned
    	mycustomstring.setString("This is a longer string.");
        assertEquals("", mycustomstring.removeEveryNthCharacter(1, false));

    }

    
    @Test
    public void testremoveEveryNthCharacter8() {
       	//Test if input string is only one letter, and n = 1. Should return empty space as long as the original string.
    	mycustomstring.setString("Strings");
        assertEquals("       ", mycustomstring.removeEveryNthCharacter(1, true));

    }

    
    @Test
    public void testremoveEveryNthCharacter9() {
    	//Test if input string length and and n are the same, the original string minus the last character should be returned.
    	mycustomstring.setString("Strings");
        assertEquals("String", mycustomstring.removeEveryNthCharacter(7, false));

    }
    
    @Test
    public void testremoveEveryNthCharacter10() {
        //Test if input string length and and n are the same, the original string minus the last character plus an empty space should be returned.
    	mycustomstring.setString("Strings");
        assertEquals("String ", mycustomstring.removeEveryNthCharacter(7, true));
    }

    @Ignore
    @Test
    public void testremoveEveryNthCharacter11() {
        fail("Not yet implemented");
    }

    @Ignore
    @Test
    public void testremoveEveryNthCharacter12() {
        fail("Not yet implemented");
    }

    
    @Test
    public void testConvertDigitsToNamesInSubstring1() {
        mycustomstring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        mycustomstring.convertDigitsToNamesInSubstring(17, 23);
        assertEquals("I'd b3tt3r put szerome done-six1ts in this 5tr1n6, right?", mycustomstring.getString());
    }

    
    @Test
    public void testConvertDigitsToNamesInSubstring2() {
    	//Test for when start and position span the entire length of the string  
    	mycustomstring.setString("I lik1 n00b3");
        mycustomstring.convertDigitsToNamesInSubstring(1, mycustomstring.getString().length());
        assertEquals("I likone nzero-zerobthree", mycustomstring.getString());
    }

    
    @Test(expected = NullPointerException.class)
    public void testConvertDigitsToNamesInSubstring3() {
    	try {
    		mycustomstring.convertDigitsToNamesInSubstring(0, 10);
    		fail();
    	}catch (Exception e){	
    		if (NullPointerException.class.isInstance(e)){
    			throw new NullPointerException();
    		}
    	}    }
    
    
    @Test(expected = IllegalArgumentException.class)
    public void testConvertDigitsToNamesInSubstring4() {
    	//Test for when startPosition is less than 1 and startPosition <= endPosition
    	try {
    		mycustomstring.setString("I lik1 n00b3");
    		mycustomstring.convertDigitsToNamesInSubstring(0, 12);
    		fail();
    	}catch (Exception e){	
    		if (IllegalArgumentException.class.isInstance(e)){
    			throw new IllegalArgumentException();
    		}
    	}    
	}

    
    
    
    @Test(expected = MyIndexOutOfBoundsException.class)
    public void testConvertDigitsToNamesInSubstring5() {
    	//Test for when endPosition is less than or equal to startPosition
    	try {
    		mycustomstring.setString("I lik1 n00b3");
    		mycustomstring.convertDigitsToNamesInSubstring(4, 2);
    		fail();
    	}catch (Exception e){	
    		if (MyIndexOutOfBoundsException.class.isInstance(e)){
    			throw new MyIndexOutOfBoundsException();
    		}
    	}       
	}

   

    @Test(expected = MyIndexOutOfBoundsException.class)
    public void testConvertDigitsToNamesInSubstring6() {
    	//Test for when endPosition is less than or equal to startPosition
    	try {
    		mycustomstring.setString("I lik1 n00b3");
    		mycustomstring.convertDigitsToNamesInSubstring(2, 15);
    		fail();
    	}catch (Exception e){	
    		if (MyIndexOutOfBoundsException.class.isInstance(e)){
    			throw new MyIndexOutOfBoundsException();
    		}
    	}       

    }

    
    
    @Test
    public void testConvertDigitsToNamesInSubstring7() {
        //Test for when the whole string is all numbers
    	mycustomstring.setString("1234");
        mycustomstring.convertDigitsToNamesInSubstring(1, mycustomstring.getString().length());
        assertEquals("one-two-three-four", mycustomstring.getString());
    }

    /*
    @Ignore
    @Test
    public void testConvertDigitsToNamesInSubstring8() {
        fail("Not yet implemented");
    }

    @Ignore
    @Test
    public void testConvertDigitsToNamesInSubstring9() {
        fail("Not yet implemented");
    }
    
    @Ignore
    @Test
    public void testConvertDigitsToNamesInSubstring10() {
        fail("Not yet implemented");
    }
	*/
}
