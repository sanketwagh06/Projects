#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cuda.h>
#include <sys/time.h>

/*
 
Aim         : To benchmark the GPU in terms of Read and Write Bandwidth with different types of block sizes.

Description : This program finds Read and Write Memory Bandwidth of GPU.
              The main function creates memory on CPU and copies to GPU, and then read memory from GPU into CPU.
              This operation is done for three types of bloxk sizes : 1B, 1KB, 1MB.
                  
Contributor : Vivek Pabani (A20332117)
*/


int main(void)
{
    double time_s;
    long start_time,end_time;
    struct timeval start,stop;

    char *host_memory;//, *dev_memory;
    
    long blockSize[3] = {1,1024,1048576};
    long limit[3] = {1000000,100000,100000};
    char blockTypes[3][20] = {"B","KB","MB"};
    char operationTypes[2][20] = {"Write","Read"};
    int i=0, j=0, k=0, numberOfBlocks = 3, numberOfOperations = 2;
            
    /*
    Operations :
    0:Write, 
    1 Read, 
    */

    for(j=0; j<numberOfOperations; ++j)
    {
        printf("\n----Operation = %s---- \n\n",operationTypes[j]);
        printf("Block Size\tTotal Data\tTotal Time ms\tBandwidth MBPS\n\n");
  
        /*
         Block Sizes :
         0 : 1 B 
         1 : 1 KB
         2 : 1 MB
         
         */
               
        for(k=0; k<numberOfBlocks; ++k)
        {
            printf("1 %s\t\t%7d %2s\t",blockTypes[k],limit[k],blockTypes[k]);

            char *dev_memory;
                    
            /* Assign the Host Memory*/    
            
            host_memory = (char*) malloc(blockSize[k]*sizeof(char)); 

            /* Assign the Device Memory*/    

            cudaMalloc((void**)&dev_memory, blockSize[k]*sizeof(char));

            /* Write Operation*/    
            
            if(j==0)
            {
                memset(host_memory,'a',blockSize[k]);

                /* Time calculation for main operation starts */    

                gettimeofday(&start,NULL);
    
                for (i=0; i<limit[k]; ++i)
                {
                    cudaMemcpy(dev_memory,&host_memory[i],blockSize[k]*sizeof(char),cudaMemcpyHostToDevice);
                }
    
                gettimeofday(&stop,NULL);

                /* Time calculation for main operation ends */    

            }
            
            /* Read Operation*/    

            else if (j==1)
            {
                cudaMemset(dev_memory,'a',blockSize[k]);

                /* Time calculation for main operation starts */    
    
                gettimeofday(&start,NULL);
    
                for (i=0; i<limit[k]; ++i)
                {
                    cudaMemcpy(host_memory,&dev_memory[i],blockSize[k]*sizeof(char),cudaMemcpyDeviceToHost);
                }
    
                gettimeofday(&stop,NULL);
                
                /* Time calculation for main operation starts */    

            }
        
            start_time=start.tv_sec*1000000 + start.tv_usec;
            end_time=stop.tv_sec*1000000 + stop.tv_usec;//get end time

            time_s=end_time-start_time;
            printf("%8.3f\t%9.5f\n",(time_s/1000),(blockSize[k]*limit[k]*1000)/(time_s*1024*1024));

            cudaFree(dev_memory);
        }
    }
        
    return 0;
}