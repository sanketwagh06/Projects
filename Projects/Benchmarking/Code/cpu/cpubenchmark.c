#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <stdlib.h>

/*
 
Aim         : To benchmark the CPU in terms of FLOPS and IOPS with different number of threads.

Description : This program finds the FLOPS and IOPS of CPU. 
              It works on four leves of concurrency : 1 Thread, 2 Threads, 4 Threads and 8 Threads. The main function decides the number of threads
              with count variable, type of operation with choice variable. The intFun and floatFun functions perform integer and floating point operations 
              for each choice of threads.

Contributor : Vivek Pabani (A20332117)
*/


#define GIGA 1024*1024*1024 

void *floatFun(void *arg);
void *intFun(void *arg);

long limit = 100000000;

void *intFun(void *arg)
{
    int *val = (int *) arg;
    long j = 0;
    int a=6, b=3, c=4, d=2, e=5, f=8, g=9, h=7;
    long local_limit = limit;
    
    for(j=0; j<local_limit ; j++)
    {
        (*val) = (a*b*c*d*e*f*g)+(b*c*d*e*f*g*h)+(a*c*d*e*f*g*h)+(a*b*d*e*f*g*h)+(a*b*c*e*f*g*h)+(a*b*c*d*f*g*h)+(a*b*c*d*e*g*h)+(a*b*c*d*e*f*h)
        +(a*b*c*d*e*f)+(b*c*d*e*f*g)+(a*c*d*e*f*g)+(a*b*d*e*f*g)+(a*b*c*e*f*g)+(a*b*c*d*f*g)+(a*b*c*d*e*g)+(a*b*c*d*e*f)
        +(a*b*c*d*e)+(b*c*d*e*f)+(a*c*d*e*f)+(a*b*d*e*f)+(a*b*c*e*f)+(a*b*c*d*f)+(a*b*c*d*g)+(a*b*c*d*h)
        +(a*b*c*d)+(b*c*d*e)+(a*c*d*e)+(a*b*d*e)+(a*b*c*e)+(a*b*c*h)+(a*b*c*g)+(a*b*c*f);	
    }
    return NULL;
}


void *floatFun(void *arg)
{
    float *val = (float *) arg;
    long j = 0;
    float a=6.5f, b=3.0f, c=4.1f, d=3.1f, e=1.9f, f=2.1f, g=2.9f, h=4.5f;
    long local_limit = limit;
    
    for(j=0; j<local_limit ; j++)
    {
        (*val) = (a*b*c*d*e*f*g)+(b*c*d*e*f*g*h)+(a*c*d*e*f*g*h)+(a*b*d*e*f*g*h)+(a*b*c*e*f*g*h)+(a*b*c*d*f*g*h)+(a*b*c*d*e*g*h)+(a*b*c*d*e*f*h)
        +(a*b*c*d*e*f)+(b*c*d*e*f*g)+(a*c*d*e*f*g)+(a*b*d*e*f*g)+(a*b*c*e*f*g)+(a*b*c*d*f*g)+(a*b*c*d*e*g)+(a*b*c*d*e*f)
        +(a*b*c*d*e)+(b*c*d*e*f)+(a*c*d*e*f)+(a*b*d*e*f)+(a*b*c*e*f)+(a*b*c*d*f)+(a*b*c*d*g)+(a*b*c*d*h)
        +(a*b*c*d)+(b*c*d*e)+(a*c*d*e)+(a*b*d*e)+(a*b*c*e)+(a*b*c*h)+(a*b*c*g)+(a*b*c*f);	
    }
    return NULL;
}

int main()
{

    float sec=0.00, loopSec=0.0, totalTime, answer;
    int msec=0, loopMsec=0;
    int i=0, k=0;
    clock_t start, diff, loopDiff;
    int *nums;
    long totalCalculations;
    int numberOfThreads[5] = {0,1,2,4,8};
    char choiceValues[3][10] = {"","IOPS","FLOPS"},operationTypes[3][15] = {"","Integer","Float"};

    int count;  /* Defines mode of multithreading - {1: One Thread, 2: Two Threads, 3: Four Threads, 4: Eight Threads} */

    int choice; /* Defines IOPS or FLOPS - {1:IOPS, 2:FLOPS} */

/*-----------------------------------------------*/

    /* Time Calculation for the empty loop */
    
    start = clock();
    
    for(k=0; k<limit;++k);
    
    loopDiff = clock() - start;
    
    loopMsec = loopDiff * 1000 / CLOCKS_PER_SEC;
    loopSec = (float)loopMsec/1000.0;
    
/*-----------------------------------------------*/
    printf("\nThreads\t\tOperation\tClaculations\t  Time(Sec)\tFLOPS/IOPS \n");

    for (count = 1; count<5; ++count) 
    {

        nums = (int*)malloc((numberOfThreads[count])*sizeof(int));  
        
        /* Thread Identifier */
        
        pthread_t *tid = malloc(numberOfThreads[count] * sizeof(pthread_t));
        
        totalCalculations = 175.0*(float)limit*numberOfThreads[count];
                  
        for(choice = 1; choice <3; ++choice)
        {
            printf("%d\t\t%s\t\t%ld\t",numberOfThreads[count],operationTypes[choice],totalCalculations);

            /* For IOPS */
            
            if (choice == 1)
            {

                /* Assign values to array of the int to be passed */
            
                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    nums[i] = i * 3;
                }
        
                /* Time Calculation Starts for the actual loop */
        
                start = clock();

                /* Creation of Threads and Execution */

                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    pthread_create(&tid[0], NULL, intFun, (void *) &nums[i]);
                }
        
                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    pthread_join(tid[i], NULL);
                }

                diff = clock() - start;

                /* Time Calculation Ends for the actual loop */
 
            }

            /* For FLOPS */

            else if (choice == 2)
            {
              
                /* Assign values to array of the int to be passed */

                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    nums[i] = i * 3.0;
                }
        
                /* Time Calculation Starts for the actual loop */
        
                start = clock();
        
                /* Creation of Threads and Execution */
        
                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    pthread_create(&tid[0], NULL, floatFun, (void *) &nums[i]);
                }

                for(i = 0 ; i < numberOfThreads[count] ; i++)
                {
                    pthread_join(tid[i], NULL);
                }

                diff = clock() - start;
        
                /* Time Calculation Ends for the actual loop */
        
            }

            /*-----------------------------------------------*/
            
            msec = diff * 1000 / CLOCKS_PER_SEC;
            sec = (float)msec/1000.0;
            
            totalTime = (float)(sec-loopSec)/numberOfThreads[count];
            answer = totalCalculations*2/((float)totalTime*(long)GIGA);

            printf("%10.5f\t%10.5f\n",totalTime,answer);             
        }
    }
    
    pthread_exit(NULL);
    free(nums);
    return 0;

}

