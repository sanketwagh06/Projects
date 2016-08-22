#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <fcntl.h>
#include <pthread.h> 
#include <string.h> 

/*
 
 Aim         : To benchmark the memory in terms of throughput(MB/sec) and latency(ms) with different number of threads.
 
 Description : This program finds the throughput and latency for different four operations : Sequential Write and Read, Random Write and Read. 
               It works on two leves of concurrency : 1 Thread and 2 Threads. The main function decides the number of threads
               with choice variable, and size of block with typeOfBlocks variable. The dataTransfer function performs all 4 mentioned operations 
               for each combination of threads and blocksize.
 
 Contributor : Vivek Pabani (A20332117)
               Sanket Nitin Wagh (A20330391)
 
 */


#define BYTE 1
#define KBYTE 1024
#define MBYTE 1024*1024

long i=0, j=0, r=0, k=0;
clock_t startTime,endTime;
double timeDifference;
float throughput, latency;
int numberOfThreads[3] = {0,1,2}, numberOfOperations = 4, typeOfBlocks = 3;
long sizeValues[3] = {1,1024,1048576}, limitValues[3]={20000000,200000,200},approxValues[3] = {1,1000,1000000};
char typeOfOperations[4][30] = {"Seq Write Operation","Seq Read Operation","Random Write Operation","Random Read Operation"};
char typeOfSizes[3][20] = {"1 Byte","1 KiloByte","1 MegaByte"};

void* dataTransfer(void *param);

struct Parameters {
    int operation;
    long size;
    long limit;
};

int main()
{
    int choice = 1, x=0 ;
    long var=0, tempSize=0, totalData=0 ;
    
    char *srcData;
    
    /*
     Choices :
     1 : Single Thread
     2 : Two Threads
     
     */

    
    for (choice = 1; choice < 3; ++choice) {

        /* Define parameters and threads based on the number of threads. */

        struct Parameters *parameters = malloc(numberOfThreads[choice] * sizeof(struct Parameters));
        
        pthread_t *tid = malloc(numberOfThreads[choice] * sizeof(pthread_t));
        
        printf("\n----Number of Threads = %d ---- \n\n",choice);

        
        /*
         Block Sizes :
         0 : 1 B 
         1 : 1 KB
         2 : 1 MB
         */        

        for (i = 0; i<typeOfBlocks; ++i) 
        {
            totalData = limitValues[i]*approxValues[i]/1000;
            
            printf("\n----Block Size = %s----Total Data = %ld MBs---- \n\n",typeOfSizes[i],totalData);
            
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
    }
    
    pthread_exit(NULL);
    
    return 0;
    
}


void* dataTransfer(void *param)
{
    struct Parameters *myParameters;
    myParameters =(struct Parameters*) param;
    
    int local_operation;
    int l,m,n;
    long local_size, local_limit;
    long random=0;
    char *src, *dst;
    
    local_operation = myParameters->operation;
    local_size = myParameters->size;
    local_limit = myParameters->limit;

    dst =(char *) malloc(sizeof(char)*local_size*local_limit);
    src =(char *) malloc(sizeof(char)*local_size*local_limit);

    for (l=0; l<local_size*local_limit; ++l) 
    {
        src[l] = (char)('a'+ (l%26));
    }
    
    //  Sequential Write Operation
    
    if (local_operation == 0)
    {    
        for (m=0; m<local_limit; ++m) 
        {
            memcpy(&dst[m*local_size],src,local_size);
        }
    }
    
    //  Sequential Read Operation
    
    else if (local_operation == 1)
    {
        for (m=0; m<local_limit; ++m) 
        {
            strncpy(dst,&src[m*local_size],local_size);
        }
    }
    
    //  Random Write Operation    
    
    else if (local_operation == 2)
    {        
        for (m=0; m<local_limit; ++m) 
        {
            random = rand()%(local_size*(local_limit-5));

            memcpy(&dst[random],src,local_size);
        }
    }
    
    //  Random Read Operation
    
    else if (local_operation == 3)
    {
        for (m=0; m<local_limit; ++m) 
        {
            random = rand()%(local_size*(local_limit-5));
            strncpy(dst,&src[random],local_size);
        }
    }
    
    return NULL;
}


