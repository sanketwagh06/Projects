package cs481.postag;

import cs481.token.*;
import cs481.util.*;

import java.io.*;
import java.util.*;

import org.w3c.dom.*;

/**
 * Find the difference between 2 token files using SubstDiff.
 * Run from the commandline.
 *
 * @author Sterling Stuart Stein
 */
public class POSDiff
{
   /**
    * Load the 2 files and compare them
    *
    * @param argv The names of the 2 file
    */
   public static void main(String[] argv) throws Exception
   {
      if(argv.length != 2)
      {
         System.err.println("Error: wrong number of arguments");
         System.err.println(
            "Format:  java cs481.postag.POSDiff <file 1> <file 2>");
         System.err.println(
            "Example: java cs481.postag.POSDiff correctanswers.xml youranswers.xml");
         System.exit(1);
      }

      Object[] t1  =
	  TokenDiff.attributeArray(Token.readXML(new BufferedInputStream(new FileInputStream(argv[0]))),
					      "pos");
      Object[] t2  = TokenDiff.attributeArray(Token.readXML(
							new BufferedInputStream(new FileInputStream(argv[1]))),
					  "pos");
      int      len = t1.length;

      if(t2.length > len)
      {
         len = t2.length;
      }

      int d = SubstDiff.diff(t1, t2);
      d = len - d;
      System.out.println("Similarity = " + d + " / " + len + " = " +
         ((100.0 * d) / len) + " %");
      /*
	Diff.printdiff(t1, t2, SubstDiff.difflist(t1, t2));
      System.out.println("Similarity = " + d + " / " + len + " = " +
         ((100.0 * d) / len) + " %");
      */
   }
}
