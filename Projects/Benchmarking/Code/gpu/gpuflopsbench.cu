#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cuda.h>
#include <sys/time.h>

/*
 
Aim         : To benchmark the GPU in terms of FLOPS and IOPS with.

Description : This program finds the FLOPS and IOPS of GPU. 
              The gpuIntFun and gpuFloatFun are the functions which perform the operation on GPU environment. 
              The host variables are first declared and initialized. Same number of variables are allocated memory on GPU, 
              and data is copied fro host to device variables.
              The result variable is the copied back to host.

Contributor : Vivek Pabani (A20332117)
*/


#define LIMIT 500

__global__ void gpuIntFun(int *a, int *b, int *c)
{
    int tid = blockIdx.x*blockDim.x+threadIdx.x;
    c[tid] = a[tid] + b[tid];
}
__global__ void gpuFloatFun(float *a, float *b, float *c)
{
    int tid = blockIdx.x*blockDim.x+threadIdx.x;
    c[tid] = a[tid] + b[tid];
}

int main(void)
{
    int numberOfThreads;
    int blocks, threads;
    int i=0;
    int choice=0;
    
    double time_s;
    long start_time,end_time;
    struct timeval start,stop;

    struct cudaDeviceProp gpuDetails;
    int numberOfDevices, device=0;

    cudaError_t cudaResultCode = cudaGetDeviceCount(&numberOfDevices);

//To get device info on run time

    for (device = 0; device < numberOfDevices; ++device) {
        cudaGetDeviceProperties(&gpuDetails, device);

//To set device variables to be used for thread creation.

        if (gpuDetails.major != 9999)
        {    
            blocks=gpuDetails.multiProcessorCount;
            threads=gpuDetails.maxThreadsPerMultiProcessor;
            numberOfThreads=blocks * threads;
        }
    }

    printf("Processor Count %d\n",blocks);
    printf("Thread per Processor %d\n",threads);
    printf("Total Threads %d\n",numberOfThreads);

    /*
    choice 
    0 - IOPS
    1 - FLOPS
    */
    
    for(choice=0; choice<2; ++choice)
    {
        if(choice == 0)
        {
            int *host_a, *host_b, *host_c;
            int *dev_a, *dev_b, *dev_c;

            //assign memory to host variables.
            
            host_a = (int*) malloc(numberOfThreads*sizeof(int)); 
            host_b = (int*) malloc(numberOfThreads*sizeof(int)); 
            host_c = (int*) malloc(numberOfThreads*sizeof(int)); 

            //Initialize host variables.
            
            for(i=0;i<numberOfThreads;++i)
            {
                host_a[i] = (i*25)+25;
                host_b[i] = (i*36)+36; 
            }

            //assign memory to device variables

            cudaMalloc((void**)&dev_a, numberOfThreads*sizeof(int));
            cudaMalloc((void**)&dev_b, numberOfThreads*sizeof(int));
            cudaMalloc((void**)&dev_c, numberOfThreads*sizeof(int));

            // copy variables to device memory
            
            cudaMemcpy(dev_a,host_a,numberOfThreads*sizeof(int),cudaMemcpyHostToDevice);
            cudaMemcpy(dev_b,host_b,numberOfThreads*sizeof(int),cudaMemcpyHostToDevice);

            //Calculation Time Starts
            
            gettimeofday(&start,NULL);
    
            start_time=start.tv_sec*1000000 + start.tv_usec;

            for (i=0; i<LIMIT; ++i)
            {
                gpuIntFun<<<blocks,threads>>>(dev_a,dev_b,dev_c);

            }
    
            gettimeofday(&stop,NULL);

            //Calculation Time Ends

            end_time=stop.tv_sec*1000000 + stop.tv_usec;//get end time

            cudaMemcpy(host_c,dev_c,numberOfThreads*sizeof(int),cudaMemcpyDeviceToHost);

            time_s=end_time-start_time;
            
            printf("\nTime taken: %lf",time_s);
            printf("\nIOPS: %lf",(double)(LIMIT*numberOfThreads*1.024*0.1048576)/(time_s*2.0));

            cudaFree(dev_a);
            cudaFree(dev_b);
            cudaFree(dev_c);
        }
       
        else if(choice == 1)
        {
            float *host_a, *host_b, *host_c;
            float *dev_a, *dev_b, *dev_c;

            host_a = (float*) malloc(numberOfThreads*sizeof(float)); 
            host_b = (float*) malloc(numberOfThreads*sizeof(float)); 
            host_c = (float*) malloc(numberOfThreads*sizeof(float)); 

            for(i=0;i<numberOfThreads;++i)
            {
                host_a[i] = (i*25.5)+25.5;
                host_b[i] = (i*36.6)+36.6; 
            }

            cudaMalloc((void**)&dev_a, numberOfThreads*sizeof(float));
            cudaMalloc((void**)&dev_b, numberOfThreads*sizeof(float));
            cudaMalloc((void**)&dev_c, numberOfThreads*sizeof(float));

            cudaMemcpy(dev_a,host_a,numberOfThreads*sizeof(float),cudaMemcpyHostToDevice);
            cudaMemcpy(dev_b,host_b,numberOfThreads*sizeof(float),cudaMemcpyHostToDevice);

            gettimeofday(&start,NULL);
    
            start_time=start.tv_sec*1000000 + start.tv_usec;

            for (i=0; i<LIMIT; ++i)
            {
                gpuFloatFun<<<blocks,threads>>>(dev_a,dev_b,dev_c);

            }
    
            gettimeofday(&stop,NULL);
            end_time=stop.tv_sec*1000000 + stop.tv_usec;//get end time

            cudaMemcpy(host_c,dev_c,numberOfThreads*sizeof(int),cudaMemcpyDeviceToHost);

            time_s=end_time-start_time;
            
            printf("\nTime taken: %lf",time_s);
            printf("\nGFLOPS: %lf\n",(double)(LIMIT*numberOfThreads*1.024*0.1048576)/(time_s*2.0));

            cudaFree(dev_a);
            cudaFree(dev_b);
            cudaFree(dev_c);

        }    


    }
    return 0;

}