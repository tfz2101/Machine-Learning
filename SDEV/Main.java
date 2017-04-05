package edu.gatech.seclass.replace;

public class Main {
    public static void main(String[] args) {
        String fileString = args[args.length-1];
        String to = args[args.length-2];
        String from = args[args.length-3];
        String output;
        int fromLength = from.length();
        Boolean w=false;
        Boolean i=false;
        Boolean f=false;
        for (int x = 0;x<args.length-3;x++){
        	if(args[x]=="-f"){
        		w = true;
        	}
        	else if (args[x]=="-i"){
        		i = true;
        	}
        	else if (args[x] =="-f"){
        		f = true;
        	}
        }
        
       
        output = fileString.replaceAll(from, to);
    	if(i){
    		from = "(?i)"+from;
    	}
    	if(w){
    		from = " "+from+" ";
    	}
    	if(f){
    		output = fileString.replaceFirst(from, to);
    	}
    	else if(!f){
    		output = output = fileString.replaceAll(from, to);
    	}	
    }

    private static void usage() {
        System.err.println("Usage: Replace [-f] [-i] [-w] <from> <to> <filename>" );
    }
}
