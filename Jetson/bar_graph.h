void bar_graph(double vec[], int length, int screen_width)
{
    for (int j = 0; j < screen_width; j++)
    {
        std::cout << "-";
    }
    
    std::cout << "\n";
    
    for (int i = 0; i < length; i++)
    {
        int current_line_width = round(screen_width*vec[i]);
        std::cout << vec[i];
        for(int j = 0; j < current_line_width; j++)
        {
            std::cout << "|";
        }
        std::cout << "\n";
    }
    for (int j = 0; j < screen_width; j++)
    {
        std::cout << "-";
    }
        std::cout << "\n";
}   

