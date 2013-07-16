/* simulater to run the FGUser simulation */

import java.io.BufferedReader;
import java.io.FileReader;
import java.awt.Color;
import java.awt.Font;
import java.io.*;

public class SimTest
{
    User[] users;
    double[] thresh;
    int[] ranks;
    
    int N;
    
    double merit1 = 0.5;
    double merit2 = 2;
    
    double alpha1 = 1; // entry cost. 1 = none.  2 is half as likely to enter
    double alpha2 = 1;
    
    double beta1 = 0.5; // leaving cost ("sticky-ness").  Similar to above.  
    double beta2 = 0.5; //If less than 1 equivalent to "staying cost" of having more than one network
    double pcost = 0.1; // probability with which someone in both networks will drop one regardless of beta
    
    double[] minR;
    
    Color[] colors;
    
    public SimTest(String socialFile, String metaFile, String networksFile)
    {
        try
        {
            DataInputStream binSocial = new DataInputStream(new BufferedInputStream(new FileInputStream(socialFile)));
            DataInputStream binMeta = new DataInputStream(new BufferedInputStream(new FileInputStream(metaFile)));
            DataInputStream binNetworks = new DataInputStream(new BufferedInputStream(new FileInputStream(networksFile)));
            
            int lengthSocial = Integer.parseInt(binSocial.readLine());
            int lengthMeta = Integer.parseInt(binMeta.readLine());
            int widthMeta = Integer.parseInt(binMeta.readLine());
            int lengthNetworks = Integer.parseInt(binNetworks.readLine());
            if (lengthSocial != lengthNetworks)
                System.err.println("THESE FILES ARE NOT COMPATIBLE!!!  YOUR PROGRAM WILL FAIL!!!");
            int[] degrees = new int[lengthSocial];
            int uc = 0;
            for (int i = 0; i < lengthSocial; i++)
            {
                degrees[i] = binSocial.readInt();
                if (degrees[i] > 0)
                    uc++;
            }
            int[] netDeg = new int[lengthNetworks];
            for (int i = 0; i < lengthNetworks; i++)
            {
                netDeg[i] = binNetworks.readInt();
            }
            for (int i = 0; i < lengthSocial; i++)
            {
                int[] friends = new int[degrees[i]];
                for (int j = 0; j < degrees[i]; j++)
                {
                    friends[j] = binSocial.readInt();
                }
                int[] networks = new int[netDeg[i]];
                for (int j = 0; j < netDeg[i]; j++)
                {
                    networks[j] = binNetworks.readInt();
                }
                
                users[i] = new User(i, 0, degrees[i], friends, 0, networks, 0, 0);
            }
            
        } catch (Exception e) {}
        
        
    }
    
    public SimTest(String socialFile) throws java.io.IOException
    {
        EndianInputStream binSocial = new EndianInputStream(new BufferedInputStream(new FileInputStream(socialFile)));
        
        int lengthSocial = Integer.parseInt(binSocial.readLine());
        N = lengthSocial;
        thresh = new double[N];
        System.out.println(lengthSocial);
        int[] degrees = new int[lengthSocial];
        users = new User[lengthSocial];
        int uc = 0;
        for (int i = 0; i < lengthSocial; i++)
        {
            degrees[i] = binSocial.readLittleInt();
            //System.out.println(degrees[i]);
            if (degrees[i] > 0)
                uc++;
        }
        for (int i = 0; i < lengthSocial; i++)
        {
            int[] friends = new int[degrees[i]];
            for (int j = 0; j < degrees[i]; j++)
            {
                friends[j] = binSocial.readLittleInt();
                //System.out.println(i + ", " + friends[j]);
            }
            users[i] = new User(i, 0, degrees[i], friends, 0, null, 0, 0);
        }
        
    }
    
    public SimTest(String f1, String f2, int s) throws java.io.IOException
    {
        N = s + 1;
        BufferedReader graph = new BufferedReader(new FileReader(f1));
        BufferedReader prop = new BufferedReader(new FileReader(f2));
        
        thresh = new double[N];
        minR = new double[N];
        for (int i = 1; i < N; i++)
        {
            thresh[i] = Math.random();
            minR[i] = (Math.random() * 2) - 1;
        }
        
        int[] temp;
        
        users = new User[N];
        for (int i = 1; i < N; i++)
        {
            // variables to go in each user node
            int id;
            int sampled;
            int[] friendIds;
            int friendCount;
            int privacy;
            int[] networkIds;
            int product1;
            int product2;
            
            // get new line from each file
            String graphs = graph.readLine();
            String props = prop.readLine();
            
            //parse graphs file
            String[] friends = graphs.split(" ");
            int n = friends.length;
            id = Integer.parseInt(friends[0]);
            sampled = Integer.parseInt(friends[1]);
            temp = new int[n - 2];
            friendCount = 0;
            for (int j = 2; j < n; j++)
            {
                int friend = Integer.parseInt(friends[j]);
                if (friend < N)
                {
                    temp[j - 2] = friend;
                    friendCount++;
                }
            }
            friendIds = new int[friendCount];
            int k = 0;
            for (int j = 0; j < n-2; j++)
            {
                if (temp[j] != 0)
                {
                    friendIds[k] = temp[j];
                    k++;
                }
            }
            
            // parse the properties file
            String[] properties = props.split("#");
            //friendCount = Integer.parseInt(properties[2]);
            privacy = Integer.parseInt(properties[3]);
            
            // only add network ID's if there are any
            if (properties.length > 4)
            {
                String[] networks = properties[4].split("\\|");
                n = networks.length;
                networkIds = new int[n];
                for (int j = 0; j < n; j++)
                    networkIds[j] = Integer.parseInt(networks[j]);
            }
            else
            {
                networkIds = null;
            }
            
            product1 = product2 = 0;
            
            users[i] = new User(id, sampled, friendCount, friendIds, privacy, networkIds, product1, product2);
        }
    }
    
    public void seedRange1(int rl, int rh)
    {
        for (int i = 1; i < N; i++)
        {
            thresh[i] = 0.3;
            if ((i > rl) && (i < rh))
                users[i].product1 = 1;
            else
                users[i].product1 = 0;
        }
    }
    
    public void seedRange2(int rl, int rh)
    {
        for (int i = 1; i < N; i++)
        {
            if ((i > rl) && (i < rh))
                users[i].product2 = 1;
            else
                users[i].product2 = 0;
        }
    }
    
    // get the averge product over all the users
    public double[] marketShares(int stepSize)
    {
        int cumprod1 = 0;
        int cumprod2 = 0;
        int uc = 0;
        double ms1 = 0;
        double ms2 = 0;
        
        for (int i = 0; i < N; i += stepSize)
        {
            if (users[i].product1 == 1)
            {
                cumprod1++;
                //System.out.println("user " + i + ", product 1"); 
            };
            if (users[i].product2 == 1)
            {
                cumprod2++;
                //System.out.println("user " + i + ", product 2"); 
            }
            uc++;
        }
        
        if (uc > 0)
        {
            ms1 = ((double) cumprod1)/uc;
            ms2 = ((double) cumprod2)/uc;
        }
        
        double[] result = new double[2];
        result[0] = ms1;
        result[1] = ms2;
        //System.out.println(cumprod1 + ", " + cumprod2);
        return result;
        
    }
    
    // move 1 step forward in sim. "rand" should be range (0-1)
    public boolean step(double rand)
    {
        if ((rand < 0) || (rand > 1))
            return false;
        
        for (int i = 0; i < N; i++)
        {
            // get friend array
            int fc = users[i].friendCount;
            int[] friends = users[i].friendIds;
            
            // count active friends for each product
            double fa1 = 0;
            double fa2 = 0;
            for (int j = 0; j < fc; j++)
            {
                if (users[friends[j]].product1 == 1)
                    fa1++;
                fa2 += users[friends[j]].product2;
            }
            
            // update using the linear threshold model with "rand" randomness
            // update - case where no products are in use
            if ((users[i].product1 + users[i].product2) == 0)
            {
                double tre = thresh[i];// (rand) * Math.random() + (1 - rand) * thresh[i];
                if (fa1/fc >= tre/merit1)
                    users[i].newProduct1 = 1;
                if (fa2/fc >= tre/merit2)
                    users[i].newProduct2 = 1;
                if ((users[i].newProduct1 == 1) && (users[i].newProduct2 == 1)) // don't join 2
                {
                    if ((fa1 * merit1) > (fa2 * merit2))
                        users[i].newProduct2 = 0;
                    else if ((fa1 * merit1) < (fa2 * merit2))
                        users[i].newProduct1 = 0;
                    else if ((fa1 * merit1) == (fa2 * merit2))
                    {
                        if (Math.random() >= 0.5)
                            users[i].newProduct2 = 0;
                        else
                            users[i].newProduct1 = 0;
                    }
                }
            }
            
            // update - case where product 1 is in use
            else if ((users[i].product1 == 1) && (users[i].product2 == 0))
            {
                double tre = thresh[i];//(rand) * Math.random() + (1 - rand) * thresh[i];
                if (fa2/fc >= (tre/merit2)*alpha2)
                {
                    users[i].newProduct2 = 1;
                    //System.out.println(fa2 + ", " + fc);
                    //System.out.println((tre/merit2)*alpha2);
                }
            }
            
            // update - case where product 2 is in use
            else if ((users[i].product2 == 1) && (users[i].product1 == 0))
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if ((fa1/fc) >= (tre/merit1)*alpha1)
                    users[i].newProduct1 = 1;
            }
            
            // update - case where both products are in use
            else
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if (fa1/fc <= (tre/merit1) * beta1)
                    users[i].newProduct1 = 0;
                if (fa2/fc <= (tre/merit2) * beta2)
                    users[i].newProduct2 = 0;
                if ((users[i].newProduct1 == 0) && (users[i].newProduct2 == 0)) // don't drop both
                {
                    if ((fa1 * merit1) > (fa2 * merit2))
                        users[i].newProduct1 = 1;
                    else if ((fa1 * merit1) < (fa2 * merit2))
                        users[i].newProduct2 = 1;
                    else if ((fa1 * merit1) == (fa2 * merit2))
                    {
                        if (Math.random() >= 0.5)
                            users[i].newProduct2 = 1;
                        else
                            users[i].newProduct1 = 1;
                    }
                }
            }
        }
        
        for (int i = 0; i < N; i++)
        {
            boolean suc = users[i].refresh();
            if (!suc)
            {
                System.err.println("---REFRESH FAILED!!!---");
                System.out.println("---REFRESH FAILED!!!---");
            }
        }
        
        return true;
    }
    
    // move 1 step forward in sim. "rand" should be range (0-1)
    public boolean stepS(double rand)
    {
        if ((rand < 0) || (rand > 1))
            return false;
        
        for (int i = 1; i < N; i++)
        {
            // get friend array
            int fc = users[i].friendCount;
            int[] friends = users[i].friendIds;
            
            // count active friends for each product
            double fa1 = 0;
            double fa2 = 0;
            for (int j = 0; j < fc; j++)
            {
                if (users[friends[j]].product1 == 1)
                    fa1++;
                fa2 += users[friends[j]].product2;
            }
            
            // update using the linear threshold model with "rand" randomness
            // update - case where no products are in use
            if ((users[i].product1 + users[i].product2) == 0)
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if (fa1/fc >= tre/merit1)
                    users[i].newProduct1 = 1;
                if (fa2/fc >= tre/merit2)
                    users[i].newProduct2 = 1;
                if ((users[i].newProduct1 == 1) && (users[i].newProduct2 == 1)) // don't join 2
                {
                    if ((fa1 * merit1) > (fa2 * merit2))
                        users[i].newProduct2 = 0;
                    else if ((fa1 * merit1) < (fa2 * merit2))
                        users[i].newProduct1 = 0;
                    else if ((fa1 * merit1) == (fa2 * merit2))
                    {
                        if (Math.random() >= 0.5)
                            users[i].newProduct2 = 0;
                        else
                            users[i].newProduct1 = 0;
                    }
                }
            }
            
            // update - case where product 1 is in use
            else if ((users[i].product1 == 1) && (users[i].product2 == 0))
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if (fa2/fc >= (tre/merit2)*alpha2)
                    users[i].newProduct2 = 1;
            }
            
            // update - case where product 2 is in use
            else if ((users[i].product2 == 1) && (users[i].product1 == 0))
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if ((fa1/fc) >= (tre/merit1)*alpha1)
                    users[i].newProduct1 = 1;
            }
            
            // update - case where both products are in use
            else
            {
                double tre = (rand) * Math.random() + (1 - rand) * thresh[i];
                if ((1 - fa1/fc) >= (tre/merit1) * beta1)
                    users[i].newProduct1 = 0;
                if ((1 - fa2/fc) >= (tre/merit2) * beta2)
                    users[i].newProduct2 = 0;
                if ((users[i].newProduct1 == 0) && (users[i].newProduct2 == 0)) // don't drop both
                {
                    if ((fa1 * merit1) > (fa2 * merit2))
                        users[i].newProduct1 = 1;
                    else if ((fa1 * merit1) < (fa2 * merit2))
                        users[i].newProduct2 = 1;
                    else if ((fa1 * merit1) == (fa2 * merit2))
                    {
                        if (Math.random() >= 0.5)
                            users[i].newProduct2 = 1;
                        else
                            users[i].newProduct1 = 1;
                    }
                }
                if ((users[i].newProduct1 == 0) && (users[i].newProduct2 == 0) && (Math.random() < pcost)) // drop at least one with probability pcost
                {
                    if ((fa1 * merit1) < (fa2 * merit2))
                        users[i].newProduct1 = 0;
                    else if ((fa1 * merit1) > (fa2 * merit2))
                        users[i].newProduct2 = 0;
                    else
                    {
                        if (Math.random() >= 0.5)
                            users[i].newProduct2 = 0;
                        else
                            users[i].newProduct1 = 0;
                    }
                    System.err.println("dropped one regardless because equal popularities");
                }
            }
        }
        
        for (int i = 1; i < N; i++)
        {
            boolean suc = users[i].refresh();
            if (!suc)
            {
                System.err.println("---REFRESH FAILED!!!---");
                System.out.println("---REFRESH FAILED!!!---");
            }
        }
        
        //System.err.print("--" + check + ", 0: " + zf + ", 1: " + f1 + ", 2: " + f2 + ", 3: " + f3 + "--");
        return true;
    }
    
    public void printProducts(int stepSize)
    {
        for (int i = 1; i < N; i += stepSize)
            System.out.println("   " + users[i].product1 + ", " + users[i].product2);
    }
    
    public void clear()
    {
        for (int i = 1; i < N; i++)
        {
            users[i].product1 = 0;
            users[i].product2 = 0;
            users[i].newProduct1 = 0;
            users[i].newProduct2 = 0;
            users[i].op1 = 0;
            users[i].op2 = 0;
            users[i].p1tried = false;
            users[i].p2tried = false;
        }
    }
    
    public int[] count()
    {
        int[] count = new int[160];
        for (int i = 1; i < N; i++)
        {
            if (users[i].friendCount < 160)
                count[users[i].friendCount]++;
            System.out.print(users[i].friendCount + ", ");
        }
        return count;
    }
    
    public static void main(String[] args) throws java.io.IOException
    {
        int size = 957359; //Integer.parseInt(args[3]);
        
        SimTest sim = new SimTest("testSocial.bin");//, "mhrw-nodeproperties.txt", size); //JPsim(args[0], args[1], args[2], size, outs);
        double[][] ms = sim.runTest(5);
    }
    
    public void setThresh(double val)
    {
        for (int i = 0; i < N; i++)
        {
            thresh[i] = val;
        }
    }
    
    public double[][] runTest(int rounds)
    {
        clear();
        double[][] ret = new double[rounds][2];
        alpha1 = 1;
        alpha2 = 1;
        beta1 = 1;
        beta2 = 1;
        merit1 = 1;
        merit2 = 2;
        pcost = 0;
        //seedRange1(1, 100000);
        //seedRange2(100000, 200000);
        users[0].setProduct1(1);
        users[3].setProduct2(1);
        setThresh(0.3);
        double[] shares = marketShares(1);
        System.out.println(shares[0] + ", " + shares[1]);
        for (int i = 0; i < rounds; i++)
        {
            boolean suc = step(0);
            if (!suc)
            {
                System.err.println("---STEP FAILED!!!---");
                System.out.println("---STEP FAILED!!!---");
            }
            
            shares = marketShares(1);
            ret[i][0] = shares[0];
            ret[i][1] = shares[1];
            System.out.println(ret[i][0] + ", " + ret[i][1]);
        }
        return ret;
    }
    
}