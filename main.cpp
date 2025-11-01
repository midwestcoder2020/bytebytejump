#include <allegro5/allegro.h>
#include <string>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <cstdio>
#include <allegro5/allegro_primitives.h>
#include <cmath>

#define UNITS 5
#define DISP_W UNITS
#define DISP_H UNITS
#define SCALE 100

void mem_dump(unsigned int mem[],int size){
    std::cout << mem[0] << " " << mem[1] << " " << mem[2] << " " << mem[3] << " " <<  mem[4] << " " << std::endl;
     std::cout << mem[5] << " " << mem[6] << " " << mem[7] << " " << mem[8] << " " <<  mem[9] << " " << std::endl;
      std::cout << mem[10] << " " << mem[11] << " " << mem[12] << " " << mem[13] << " " <<  mem[14] << " " << std::endl;
       std::cout << mem[15] << " " << mem[16] << " " << mem[17] << " " << mem[18] << " " <<  mem[19] << " " << std::endl;
        std::cout << mem[20] << " " << mem[21] << " " << mem[22] << " " << mem[23] << " " <<  mem[24] << " " << std::endl;
         std::cout << mem[25] << " " << mem[26]<< std::endl;
}

int main(int argc,char* argv[]){
    bool debug=false;
    std::string rom_name;
    if(argc <2){
        std::cout << "no rom provided!" << std::endl;
        return -1;
    }else{
        std::cout << "opening rom " << argv[1] << std::endl;
        rom_name=argv[1];
    }

    if(argc>2 && std::strcmp(argv[2],"debug")==0){
        debug=true;
    }

    al_init();

    int W=DISP_W;
    int H=DISP_H;
    int DS=SCALE;
    int F_SIZE=DS*W;
    int pc=0;

    int mem_size=(W*H)+2;

    unsigned int mem[mem_size];
    unsigned int buff[mem_size];

    memset(mem,0,sizeof(mem));
    memset(buff,0,sizeof(buff));

    mem[0]=0;
    mem[1]=1;

    //load rom data
    std::ifstream romfile;
    romfile.open(rom_name);

    std::vector<std::string> progam_code;

    if(romfile.is_open()){
        std::string fval;
        char rom_char1,rom_char2,rom_char3;
        
        while(romfile){
            rom_char1 = romfile.get();
            rom_char2 = romfile.get();
            rom_char3 = romfile.get();
            
            fval.push_back(rom_char1);
            fval.push_back(rom_char2);
            fval.push_back(rom_char3);
            progam_code.push_back(fval);
            fval.clear();
 
        }   

    }else{
        std::cout << "unable to open file" << std::endl;
    }

    al_init();

    al_init_primitives_addon();

    ALLEGRO_TIMER* timer = al_create_timer(1.0 / 2.5);
    ALLEGRO_EVENT_QUEUE* queue = al_create_event_queue();

    ALLEGRO_DISPLAY* disp = al_create_display(F_SIZE, F_SIZE);

    al_register_event_source(queue, al_get_display_event_source(disp));
    al_register_event_source(queue, al_get_timer_event_source(timer));

    bool redraw = true;
    bool done = false;
    ALLEGRO_EVENT event;
    int x1,x2,y1,y2=0;

    al_start_timer(timer);

    while(1)
    {

        al_wait_for_event(queue, &event);
        switch(event.type)
        {
            case ALLEGRO_EVENT_TIMER:
                redraw = true;
                break;

            case ALLEGRO_EVENT_KEY_DOWN:
            case ALLEGRO_EVENT_DISPLAY_CLOSE:
                done = true;
                break;
        }

        if(done){
            break;
        }

        if(redraw && al_is_event_queue_empty(queue))
        {
            if(debug)mem_dump(mem,mem_size);

            //do memory cycle
            int x=2;
            if(debug){
            std::cout<< "-------"<<std::endl;
            }
            while(x<mem_size){
                
                //convert from hex to int
                std::string v=progam_code[pc];
                

                if(v == "999"){
                    pc=0;
                    x=2;
                    // continue;
                    break;
                }

                if(v == "888"){
                    continue;
                }
                
                int val =std::stoi(v,nullptr,16);
                int dest = val & 0xff;
                int src = val >> 8;

                mem[dest] = mem[src];

                if(debug){
                std::cout << v << " : "<< val << " : " << src << " ->  " << dest << std::endl;
                }

                pc+=1;

                x++;
            }
            
            if(debug){
            std::cout<< "-------"<<std::endl;
            getchar();
            }

            al_clear_to_color(al_map_rgb(0, 0, 0));

            for(int x=0;x<(mem_size);x++){
                    x1 = (x%W)*DS;
                    y1 = std::ceil(x/W)*DS;
                    x2=(x1*DS)+DS;
                    y2=(y1*DS)+DS;

                    if(debug){
                    std::cout << "x1: "<<x1 << " x2: "<<x2 << " y1 " << y1 << " y2 " << y2 <<std::endl;
                    }
                    int val = mem[x+2];

                    if(val == 1){               
                         al_draw_filled_rectangle(x1,y1,x2,y2,al_map_rgb(255,255,255));
                    }else if(val== 0){
                         al_draw_filled_rectangle(x1,y1,x2,y2,al_map_rgb(0,0,0));                    
                        }  
            }
            al_flip_display();
            redraw = false;
        }
    }

    al_destroy_display(disp);
    al_destroy_timer(timer);
    al_destroy_event_queue(queue);

    return 0;
}