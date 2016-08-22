#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <fcntl.h>
#include <pthread.h> 

/*

Aim         : To benchmark the disk in terms of throughput(MB/sec) and latency(ms) with different number of threads.

Description : This program finds the throughput and latency for different four operations : Sequential Write and Read, Random Write and Read. 
              It works on three leves of concurrency : 1 Thread, 2 Threads and 4 Threads. The main function decides the number of threads
              with choice variable, and size of block with typeOfBlocks variable. The dataTransfer function performs all 4 mentioned operations 
              for each combination of threads and blocksize.

Contributor : Vivek Pabani (A20332117)
 
*/


#define BYTE 1
#define KBYTE 1024
#define MBYTE 1024*1024

void* dataTransfer(void *param);

struct Parameters {
    int operation;
    long size;
    long limit;
    FILE *fp;
};

int main()
{
    int choice=1 ;
    long var=0, r=0, i=0, j=0, k=0;
    FILE *readFile;
    
    int numberOfThreads[4] = {0,1,2,4}, numberOfOperations = 4, typeOfBlocks = 3;
    long sizeValues[3] = {1,1024,1048576}, limitValues[3]={20000000,200000,2000}, approxValues[3]={1,1000,1000000};
    
    char typeOfOperations[4][30] = {"Seq Write Operation","Seq Read Operation","Random Write Operation","Random Read Operation"};
    char typeOfSizes[3][20] = {"1 Byte","1 KiloByte","1 MegaByte"};
    
    clock_t startTime,endTime;

    double timeDifference;
    float throughput, latency;
    
    char *readData;
    readData = (char *)malloc(sizeof(char)*1024*1024);

    /* Create Data to write on the readfile*/    
    
    for (var=0; var<1048576; ++var) 
    {
        readData[var] = (char)('a'+ (var%26));
    }
    
    /*
     Choices :
     1 : Single Thread
     2 : Two Threads
     3 : Four Threads
 
     */
    for (choice=1; choice<4; ++choice) {
        
        /* Define parameters and threads based on the number of threads. */
        
        struct Parameters *parameters = malloc(numberOfThreads[choice] * sizeof(struct Parameters));
        
        pthread_t *tid = malloc(numberOfThreads[choice] * sizeof(pthread_t));

        printf("\n----Number of Threads = %d ---- \n\n",numberOfThreads[choice]);
        printf("-------Creating the ReadFile - input.txt------- \n");

        /* Create Readfile */    

        readFile = fopen("input.txt","w+");
        
        for (var=0; var<100; ++var) 
        {
            fwrite(readData,1,1048576,readFile);
        }

        /*
         Block Sizes :
         0 : 1 B 
         1 : 1 KB
         2 : 1 MB
         
         */

        for (i = 0; i<typeOfBlocks; ++i) 
        {
            printf("\n----Block Size = %s----Total Data = %ld MBs---- \n\n",typeOfSizes[i],limitValues[i]*approxValues[i]/1000);
            printf("Operation\t\tTime(Sec)\t Throughput(MB/Sec)\tLatency(ms) \n");

            /*
             Operations :
             0:Sequential Write, 
             1:Sequential Read, 
             2:Random Write, 
             3:Random Read 
             */
            
            for (j=0; j<numberOfOperations; ++j) 
            {
                for (k=0; k<numberOfThreads[choice]; ++k) 
                {
                    /* Initialize the Parameters*/    
                    parameters[k].size = sizeValues[i];
                    parameters[k].limit = limitValues[i];
                    parameters[k].operation = j;
                }
                
                /* Time calculation for main operation starts */    

                startTime = clock();
                
                /* Initialize and execute the Threads*/    

                for (k=0; k<numberOfThreads[choice]; ++k) 
                {
                    pthread_create(&tid[k], NULL, dataTransfer,(void *) &parameters[k]);

                }

                for (k=0; k<numberOfThreads[choice]; ++k) 
                {
                    pthread_join(tid[k], NULL );
                
                }
            
                endTime = clock();
                /* Time calculation for main operation ends */    

                timeDifference=((float)(endTime-startTime)/(CLOCKS_PER_SEC*numberOfThreads[choice]));
                throughput = (float) (limitValues[i]*sizeValues[i])/(MBYTE*timeDifference);
                latency = (float)(timeDifference*1000/limitValues[i]);               
                printf("%s\t%f \t %f\t\t%f \n",typeOfOperations[j],timeDifference,throughput,latency);            
            }
        }
        remove("output.txt");
        remove("input.txt");
    }
    
    pthread_exit(NULL);

    return 0;
    
}


void* dataTransfer(void *param)
{
    struct Parameters *myParameters;
    myParameters =(struct Parameters*) param;
    
    char *data;
    int local_operation;
    int l,m,n;
    long local_size, local_limit, r=0;
    FILE *local_file;
    
    local_operation = myParameters->operation;
    local_size = myParameters->size;
    local_limit = myParameters->limit;

    data = (char *)malloc(sizeof(char) * local_size);

    for (l=0; l<local_size; ++l) 
    {
        data[l] = (char)('a'+ (l%26));
    }

    
    //  Sequential Write Operation
    
    if (local_operation == 0)
    {    
        local_file = fopen("output.txt","w+");

        for (m=0; m<local_limit; ++m) 
        {
            fwrite(data,1,local_size,local_file);
        }
    }

    //  Sequential Read Operation

    else if (local_operation == 1)
    {
        local_file = fopen("input.txt","r+");
        
        for (m=0; m<local_limit; ++m) 
        {
            fread(data,1,local_size,local_file);
        }
    }
    
    //  Random Write Operation    
    
    else if (local_operation == 2)
    {
        local_file = fopen("output.txt","w+");
 
        for (m=0; m<local_limit; ++m) 
        {
            r = rand()%local_size;
            
            fseek(local_file,r,SEEK_SET); 	 	
            fwrite(data,1,local_size,local_file);
        }
    }
    
    //  Random Read Operation
    
    else if (local_operation == 3)
    {
        local_file = fopen("input.txt","r+");
        
        for (m=0; m<local_limit; ++m) 
        {
            r = rand()%local_size;
            
            fseek(local_file,r,SEEK_SET); 	 	
            fread(data,1,local_size,local_file);
        }
    }
    
    return NULL;
}
