package cs481.postag;

import cs481.token.*;
import cs481.util.*;

import java.io.*;
import java.util.*;

/**
 * Determines the part of speech tags based on Viterbi.
 *
 * <pre>
 * Typical use:
 * POSTag pt = new POSTag();
 * pt.train(training);
 * pt.tag(testing);
 * </pre>
 *
 * Run from the commandline.
 *
 * @author Sterling Stuart Stein
 * @author Shlomo Argamon
 */
public class POSTag1
{
    /**
     * Special start tag
     */
    public static String StartTag = "*START*";
    
    /**
     * Small probability for when not found
     */
    public static float epsilon = -10000000f;
    
    /**
     * Array of all tags
     */
    protected String[] tags;
    
    /**
     * Probability of tags given specific words
     */
    protected HashMap pTagWord;
    
    /**
     * Probability of individual tags (i.e., P(tag)
     */
    protected HashMap pTag;	
    
    /**
     * Hashmap of all known words
     */
    protected HashMap pTag_1;	
    
    /**
     * Hashmap of all transition probabilities. Probability of ti of first word to tj of second word.
     */

    protected HashMap allWords;;	
    
    /**
     * Make an untrained part of speech tagger.
     */
    public POSTag1()
    {
	pTagWord    = new HashMap();
	pTag        = new HashMap();
	pTag_1		= new HashMap();
	allWords    = new HashMap();
    }
    
    /**
     * Remove all training information.
     */
    public void clear()
    {
	pTag.clear();
	pTagWord.clear();
	pTag_1.clear();
	allWords.clear();
	tags = null;
    }
    
    /**
     * Increment the count in a HashMap for t.
     *
     * @param h1 The HashMap to be modified
     * @param t  The key of the field to increment
     */
    protected void inc1(HashMap h1, String t)
    {
	if(h1.containsKey(t))
	    {
		int[] ip = (int[])h1.get(t);  //Used as int *
		ip[0]++;
	    }
	else
	    {
		int[] ip = new int[1];
		ip[0] = 1;
		h1.put(t, ip);
	    }
    }
    
    /**
     * Increment the count in a HashMap for [t1,t2].
     *
     * @param h2 The HashMap to be modified
     * @param t1 The 1st part of the key of the field to increment
     * @param t2 The 2nd part of the key of the field to increment
     */
    protected void inc2(HashMap h2, String t1, String t2)
    {
	//Have to use Vector because arrays aren't hashable
	Vector key = new Vector(2);
	key.setSize(2);
	key.set(0, t1);
	key.set(1, t2);
	
	if(h2.containsKey(key)) {
		int[] ip = (int[])h2.get(key);  //Used as int *
		ip[0]++;
	} else {
		int[] ip = new int[1];
		ip[0] = 1;
		h2.put(key, ip);
	    }
    }
    /**
     * Increment the count in a HashMap for [t1,t2].
     *
     * @param h2 The HashMap to be modified
     * @param ti The previous tag.
     * @param tj The next tag.
     */
    protected void inc3(HashMap h3, String ti, String tj)
    {
	//Have to use Vector because arrays aren't hashable
	Vector key = new Vector(2);
	key.setSize(2);
	key.set(0, ti);
	key.set(1, tj);
	
	if(h3.containsKey(key)) {
		int[] ip = (int[])h3.get(key);  //Used as int *
		ip[0]++;
	} else {
		int[] ip = new int[1];
		ip[0] = 1;
		h3.put(key, ip);
	    }
    }
    
    /**
     * Train the part of speech tagger.
     *
     * @param training A vector of paragraphs which have tokens with the attribute &quot;pos&quot;.
     */
    public void train(Vector training)
    {
	int cTokens = 0;
	HashMap cWord    = new HashMap();
	HashMap cTag     = new HashMap();
	HashMap cTag_1	 = new HashMap();
	HashMap cTagWord = new HashMap();
	boolean[] bTrue = new boolean[1];
	bTrue[0] = true;
	
	clear();

	//Count word and tag occurrences
	for(Iterator i = training.iterator(); i.hasNext();) {
		Vector para = (Vector)i.next();
		
		for(Iterator j = para.iterator(); j.hasNext();) {
			Vector sent    = (Vector)j.next();
			String curtag  = StartTag;
			inc1(cTag, curtag);
			
			for(Iterator k = sent.iterator(); k.hasNext(); ) {
				Token tok = (Token)k.next();
				
				String previous_tag = curtag;
				
				curtag = (String)tok.getAttrib("pos");
				inc1(cTag, curtag);
				
				String name = tok.getName().toLowerCase();
				inc1(cWord, name);
				allWords.put(name, bTrue);
				inc2(cTagWord, curtag, name);
				cTokens++;
				inc3(cTag_1, previous_tag, curtag);
			    }
		    }
	    }
	
	//Find probabilities from counts
	for(Iterator i = cTag.keySet().iterator(); i.hasNext();) {
	    String key   = (String)i.next();
	    int[]  count = (int[])cTag.get(key);
	    pTag.put(key, new Float(Math.log(((float)count[0]) / (float)cTokens)));
	}
	
	for(Iterator i = cTagWord.keySet().iterator(); i.hasNext();) {
	    Vector key   = (Vector)i.next();
	    int[]  count = (int[])cTagWord.get(key);
	    int[]  total = (int[])cWord.get(key.get(1));

	    pTagWord.put(key, new Float(Math.log(((float)count[0]) / ((float)total[0]))));
	}
	//Make list of all possible tags
	tags = (String[])cTag.keySet().toArray(new String[0]);
	
    for(Iterator i = cTag_1.keySet().iterator(); i.hasNext();) {
	    Vector key   = (Vector)i.next();
	    int[]  count = (int[])cTag_1.get(key);
	    int[]  total = (int[])cTag.get(key.get(0));

	    //pTag_1.put(key, new Float(Math.log((float)count[0]+1) / (float)total[0]+tags.length));
	    pTag_1.put(key, new Float(Math.log((((float)count[0])+1) / (((float)total[0]+tags.length)))));
	}
    }
    
    /**
     * Print out a HashMap<Vector,int[1]>.
     *
     * @param h The HashMap to be printed.
     */
    protected void debugPrintHashInt(HashMap h) {
	for(Iterator i = h.keySet().iterator(); i.hasNext();) {
	    Vector key = (Vector)i.next();
	    int[]  ip  = (int[])h.get(key);
	    
	    for(int j = 0; j < key.size(); j++) {
		System.out.print(", " + key.get(j));
	    }
	    
	    System.out.println(": " + ip[0]);
	}
    }
    
    /**
     * Print out a HashMap<Vector,Float>.
     *
     * @param h The HashMap to be printed.
     */
    protected void debugPrintHashFloat(HashMap h) {
	for(Iterator i = h.keySet().iterator(); i.hasNext();) {
		Vector key = (Vector)i.next();
		float  f   = ((Float)h.get(key)).floatValue();
		
		for(int j = 0; j < key.size(); j++) {
			System.out.print(", " + key.get(j));
		    }
		
		System.out.println(": " + f);
	    }
    }

    protected void debugPrintHashKeys(HashMap h) {
	for(Iterator i = h.keySet().iterator(); i.hasNext();) {
	    String key = ((String)i.next());
	    System.out.println(": " + key);
	}
    }
    
    
    /**
     * Tags a sentence by setting the &quot;pos&quot; attribute in the Tokens.
     *
     * @param sent The sentence to be tagged.
     */
    public void tagSentence(Vector sent) {
	int len     = sent.size();
	if (len == 0) {
	    return;
	}
	
	int numtags = tags.length;
	System.out.println(numtags);
	
	float smoothing = (float) Math.log(1/(float)numtags);
	System.out.println(smoothing);
	
	Vector twkey = new Vector(2); //tag-word
	twkey.setSize(2);
	
	Vector tagtagkey = new Vector(2); //tag-tag
	tagtagkey.setSize(2);
	
	//Probability of best path to word with tag
	float[][] pathprob = new float[len + 1][numtags]; 
	
	//  Edge to best path to word with tag
	int[][]   backedge = new int[len + 1][numtags];
	
	String previous_tag1; //for the next tag
	int backtrack = 0; // to be used for backtracking.
	//For words in sentence
	for(int i = 0; i < pathprob.length - 1; i++) {
	    String word = ((Token)sent.get(i)).getName().toLowerCase();
	    twkey.set(1, word);

	    //Loop over tags for this word
	    for(int j = 0; j < numtags; j++) {
	    	if (j == 0){
	    		previous_tag1 = StartTag;
	    	}
	    	else{
	    		previous_tag1 = tags[backtrack];
	    	}
	    tagtagkey.set(0,previous_tag1);
	    	
	    	String thistag = tags[j];
		Float tagProb = (Float)pTag.get(thistag);
		float tagProbtag = (tagProb == null) ? epsilon : tagProb.floatValue();
		twkey.set(0, thistag);
		
		/*String thistag1 = tags[j];
			Float tagProb11 = (Float)pTag.get(thistag1);
			float tagProbtag= (tagProb11 == null) ? epsilon : tagProb11.floatValue();
			twkey.set(0, thistag1);
		*/	
			tagtagkey.set(1, thistag);
		
		boolean[] knownWord = (boolean[])allWords.get(word);
		Float twp1 = (Float)pTagWord.get(twkey);
		float twp  = (((knownWord == null)||(knownWord[0] != true)) ?
			      tagProb : 
			      ((twp1 == null) ?
			       epsilon :
			       twp1.floatValue()));
		
		Float tag_1_Prob1 = (Float)pTag_1.get(tagtagkey);
		float tag_1_Prob = (tag_1_Prob1 == null) ? smoothing : tag_1_Prob1.floatValue();
		
		// In a unigram model, only the current probability matters
		pathprob[i][j]    = twp+tag_1_Prob;

		// Now create the back link to the max prob tag at the previous stage
		// If we are at the second word or further
		if (i > 0) {
		    float max  = -100000000f;
		
		    //Loop over previous tags
		    for(int k = 0; k < numtags; k++) {
			String prevtag = tags[k];
		    
			// Probability for path->prevtag k + thistag j->word i
			float test = pathprob[i-1][k];
		    
			String prevword = ((Token)sent.get(i-1)).getName().toLowerCase();

			if (test > max) {
			    max     = test;
			    backtrack    = k;
			}
		    }
		    backedge[i][j]    = backtrack;
		    
		    Token tok = (Token)sent.get(i-1);
			tok.putAttrib("pos", tags[backtrack]);
		  
		}
	    }
	}

	//Trace back finding most probable path ... removed
	    //Follow back edges to start tag and set tags on words
    }
    
    /**
     * Tags a Vector of paragraphs by setting the &quot;pos&quot; attribute in the Tokens.
     *
     * @param testing The paragraphs to be tagged.
     */
    public void tag(Vector testing) {
	for(Iterator i = testing.iterator(); i.hasNext();) {
	    Vector para = (Vector)i.next();
	    
	    for(Iterator j = para.iterator(); j.hasNext();) {
		Vector sent = (Vector)j.next();
		tagSentence(sent);
	    }
	}
    }
    
    /**
     * Train on             the 1st XML file,
     * tag                  the 2nd XML file,
     * write the results in the 3rd XML file.
     *
     * @param argv An array of 3 XML file names.
     */
    public static void main(String[] argv) throws Exception
    {
	if(argv.length != 3) {
	    System.err.println("Wrong number of arguments.");
	    System.err.println(
			       "Format:  java cs481.postag.POSTag <train XML> <test XML> <output XML>");
	    System.err.println(
			       "Example: java cs481.postag.POSTag train.xml untagged.xml nowtagged.xml");
	    System.exit(1);
	}
	
	Vector training = Token.readXML(new BufferedInputStream(
								new FileInputStream(argv[0])));
	System.out.println("Read training file.");
	
	POSTag1 pt = new POSTag1();
	pt.train(training);
	System.out.println("Trained.");
	training = null;  //Done with it, so let garbage collector reclaim
	
	Vector testing = Token.readXML(new BufferedInputStream(
							       new FileInputStream(argv[1])));
	System.out.println("Read testing file.");
	pt.tag(testing);
	System.out.println("Tagged.");
	Token.writeXML(testing,
		       new BufferedOutputStream(new FileOutputStream(argv[2])));
    }
}
