#include <iostream>
#include "consoleSetting.h"
#include "normalMode.h"
#include <queue>
#include <conio.h>
#include <Windows.h>
#include <stdlib.h>
#include <time.h>
#include <mmsystem.h>
#include "sound.h"

using namespace std;


int dx[] = { 0 , 1 , 0 ,-1 };
int dy[] = { -1, 0, 1, 0 };


//to check 2 cells do they have same value and valid path
bool beTheSame(int** Pikachu, Point& start, Point end, char bgr[81][17])
{
	//retun if they are one
	if (start.x == end.x && start.y == end.y)
	{
		warning(Pikachu, start, end);
		return false;
	}

	//return if they donot have same value
	if (Pikachu[start.x][start.y] != Pikachu[end.x][end.y])
	{
		warning(Pikachu, start, end);
		return false;
	}

	int line[65];

	//creat board to use dfs
	int** temp = Double(Pikachu);

	if (dfs(temp, start, end, line, 0, true))
	{
		//if valid path, 2 value will be delete
		PokemonDie(Pikachu, start, end, bgr);
		deleteAll(temp);
		return true;
	}
	else
	{
		//if not valid path, return
		warning(Pikachu, start, end);
		deleteAll(temp);
		return false;
	}

	
}

//to creat random value
void spawnPokemon(int**& Pikachu)
{
	srand(time(NULL));

	//creat board
	Pikachu = new int* [WIDTH + 2];
	for (int i = 0; i < WIDTH + 2; i++)
		Pikachu[i] = new int[HEIGHT + 2];

	//put 0 value in each cell
	for (int i = 0; i < WIDTH + 2; i++)
	{
		for (int j = 0; j < HEIGHT + 2; j++)
		{
			Pikachu[i][j] = 0;
		}
	}

	//to count enough pairs
	int flagNum = WIDTH * HEIGHT / 2;

	while (flagNum > 0)
	{
		//random value
		int res = (flagNum / 3) * 3 + 65;
		int temp = 2;

		while (temp > 0)
		{
			//random location
			int idx = rand() % WIDTH + 1;
			int idy = rand() % HEIGHT + 1;
			if (Pikachu[idx][idy] == 0)
			{
				Pikachu[idx][idy] = res;
				temp--;
			}

		}
		flagNum--;
	}
	return;

}

//delocated board
void deleteAll(int**& Pikachu)
{
	for (int i = 0; i < WIDTH + 2; i++)
		delete[] Pikachu[i];
	delete[] Pikachu;
}

//draw box with data
void drawPikachu(int** Pikachu)
{
	for (int i = 1; i <= WIDTH; i++)
	{
		for (int j = 1; j <= HEIGHT; j++)
		{
			Box(Pikachu[i][j], i, j, BLACK, Pikachu[i][j] % 4 + 2);
		}
	}

	//draw HOW TO PLAY
	gotoxy(100, 12);
	cout << "PRESS";
	set_color(BLACK * 4 + RED);
	cout << " SPACE ";
	set_color(BLACK * 4 + WHITE);
	cout << "KEY TO HELP";
	gotoxy(100, 13);
	cout << "PRESS ";
	set_color(BLACK * 4 + RED);
	cout<< "ARROW";
	set_color(BLACK * 4 + WHITE);
	cout << " KEYS TO MOVE";
	gotoxy(100, 14);
	cout << "PRESS";
	set_color(BLACK * 4 + RED);
	cout << " ENTER ";	
	set_color(BLACK * 4 + WHITE);
	cout << "KEY TO CHOOSE";
	gotoxy(100, 15);
	cout << "PRESS";
	set_color(BLACK * 4 + RED);
	cout << " ESC ";
	set_color(BLACK * 4 + WHITE);
	cout << " KEYS TO EXIT";
}

//return true if input point exist
bool exist(Point p)
{
	if (p.x < 0) return false;
	if (p.y < 0) return false;
	if (p.x > WIDTH + 1) return false;
	if (p.y > HEIGHT + 1) return false;
	return true;
}

//return true if path is valid
bool checkLine(int line[65], int n)
{
	int cnt = 1;
	for (int i = 1; i < n; i++)
	{
		if (line[i] != line[i - 1]) cnt++;
	}
	if (cnt > 3) return false;
	return true;
}

//duplicate board
int** Double(int** ver)
{
	int** res = new int* [WIDTH + 2];
	for (int i = 0; i < WIDTH + 2; i++)
		res[i] = new int[HEIGHT + 2];
	for (int i = 0; i < WIDTH + 2; i++)
	{
		for (int j = 0; j < HEIGHT + 2; j++)
		{
			res[i][j] = ver[i][j];
		}
	}
	return res;
}

//funtions to handle when 1 pair is valid, and redraw background
void PokemonDie(int** Pikachu, Point& start, Point end, char bgr[81][17])
{
	//set data to 0
	Pikachu[start.x][start.y] = 0;
	Pikachu[end.x][end.y] = 0;

	Point temp;

	set_color(BLACK * 4 + GREEN);
	//travel into each cell
	for (int t = 1; t <= WIDTH;t++)
	{
		for (int k = 1; k <= HEIGHT;k++)
		{
			//to check around a cell
			if (Pikachu[t][k] != 0) continue;
			temp.x = t;
			temp.y = k;
			temp.x = 10 * temp.x;
			temp.y = 3 + 4 * temp.y;

			int n[4];
			for (int h = 0; h < 4; h++)
			{
				Point line;
				line.x = t + dx[h];
				line.y = k + dy[h];
				if (!exist(line) || Pikachu[line.x][line.y] == 0)
				{
					n[h] = -1;
				}
				else
				{
					n[h] = 0;
				}

			}
			if (n[1] == -1) n[1] = 1;
			if (n[2] == -1) n[2] = 1;

			//redraw background
			for (int i = 1 + n[0]; i < 4 + n[2]; i++)
			{
				for (int j = 1 + n[3]; j < 10 + n[1];j++)
				{
					gotoxy(temp.x + j, temp.y + i);
					if (temp.x + j == 11) cout << " ";
					else cout << bgr[temp.x + j - 10][temp.y + i - 7];
				}
			}
		}
	}
	set_color(BLACK * 4 + WHITE);
}


//draw connection to 2 cells
void path(Point end, int line[65], int n)
{
	int tempx, tempy;
	
	set_color(BLACK * 4 + YELLOW);

	if (n > 1)
	{
		//draw line in the first -> <- ^ v
		if (line[n - 1] == 2)
		{
			char ch = 24;
			tempx = end.x * 10 + 5;
			tempy = 3 + 4 * end.y - 1;
			gotoxy(tempx, tempy);
			cout << "V";
			gotoxy(tempx, tempy - 1);
			cout << "|";
			end.y--;
		}
		else if (line[n - 1] == 0)
		{
			end.y++;
			tempx = end.x * 10 + 5;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy - 1);
			cout << "^";
			gotoxy(tempx, tempy);
			cout << "|";

		}
		else if (line[n - 1] == 1)
		{
			tempx = end.x * 10 - 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx - 4, tempy);
			cout << "---->";
			end.x--;
		}
		else
		{
			end.x++;
			tempx = end.x * 10 + 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "<----";

		}

		//draw line between first and last
		for (int i = n - 2; i > 0; i--)
		{
			//0: up
			//3:right
			//2: down
			//1: left
			if (line[i] == 3)//right
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				gotoxy(tempx + 1, tempy);
				cout << "----------";
				end.x++;

			}
			else if (line[i] == 0)//down
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 3;
				for (int i = 0; i < 4; i++)
				{
					gotoxy(tempx, tempy + i);
					cout << "|";
				}
				end.y++;
			}
			else if (line[i] == 2)//up
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				for (int i = -4; i < 1; i++)
				{
					gotoxy(tempx, tempy + i);
					cout << "|";
				}
				end.y--;
			}
			else if (line[i] == 1)
			{

				end.x--;
				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				gotoxy(tempx, tempy);
				cout << "----------";

			}

		}
		
		//draw line for the last
		if (line[0] == 0)
		{
			char ch = 25;
			end.x++;
			end.y++;
			int tempx = end.x * 10 - 5;
			int tempy = 3 + 4 * end.y - 1;
			gotoxy(tempx, tempy);
			cout << "V";
			gotoxy(tempx, tempy - 1);
			cout << "|";
		}
		else if (line[0] == 2)
		{

			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * end.y + 1;
			gotoxy(tempx, tempy);
			cout << "^";
			gotoxy(tempx, tempy + 1);
			cout << "|";

		}
		else if (line[0] == 3)
		{
			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "---->";
			end.x++;
		}
		else
		{

			tempx = end.x * 10 + 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "<----";
		}

	}
	//in case two cells is next to together
	else
	{
		if (line[0] == 0)
		{
			
			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * (end.y + 1) - 1;
			gotoxy(tempx, tempy);
			cout << "^";
			gotoxy(tempx, tempy + 1);
			cout << "|";
			gotoxy(tempx, tempy + 2);
			cout << "V";
		}
		else if (line[0] == 2)
		{
			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * (end.y ) - 1;
			gotoxy(tempx, tempy);
			cout << "^";
			gotoxy(tempx, tempy + 1);
			cout << "|";
			gotoxy(tempx, tempy + 2);
			cout << "V";
		}
		else if (line[0] == 3)
		{
			int tempx = (end.x + 1) * 10 - 1;
			int tempy = 5 + 4 * (end.y);
			gotoxy(tempx, tempy);
			cout << "<->";
		}
		else if (line[0] == 1)
		{
			int tempx = (end.x) * 10 - 1;
			int tempy = 5 + 4 * (end.y);
			gotoxy(tempx, tempy);
			cout << "<->";
		}
	}
	set_color(BLACK * 4 + WHITE);
}

//delete connection to 2 cells and redraw background
//be the same as void path()
void deletePath(Point end, int line[65], int n)
{
	int tempx, tempy;

	if (n > 1)
	{
		if (line[n - 1] == 2)
		{
			tempx = end.x * 10 + 5;
			tempy = 3 + 4 * end.y - 1;
			gotoxy(tempx, tempy);
			cout << " ";
			gotoxy(tempx, tempy - 1);
			cout << " ";
			end.y--;
		}
		else if (line[n - 1] == 0)
		{
			end.y++;
			tempx = end.x * 10 + 5;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy - 1);
			cout << " ";
			gotoxy(tempx, tempy);
			cout << " ";

		}
		else if (line[n - 1] == 1)
		{
			tempx = end.x * 10 - 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx - 4, tempy);
			cout << "     ";
			end.x--;
		}
		else
		{
			end.x++;
			tempx = end.x * 10 + 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "     ";

		}
		for (int i = n - 2; i > 0; i--)
		{
			//0: up
			//3:right
			//2: down
			//1: left
			if (line[i] == 3)//right
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				gotoxy(tempx + 1, tempy);
				cout << "          ";
				end.x++;

			}
			else if (line[i] == 0)//down
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 3;
				for (int i = 0; i < 4; i++)
				{
					gotoxy(tempx, tempy + i);
					cout << " ";
				}
				end.y++;
			}
			else if (line[i] == 2)//up
			{

				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				for (int i = -4; i < 1; i++)
				{
					gotoxy(tempx, tempy + i);
					cout << " ";
				}
				end.y--;
			}
			else if (line[i] == 1)
			{

				end.x--;
				int tempx = end.x * 10 + 5;
				int tempy = 3 + 4 * end.y + 2;
				gotoxy(tempx, tempy);
				cout << "          ";

			}

		}
		if (line[0] == 0)
		{
			char ch = 25;
			end.x++;
			end.y++;
			int tempx = end.x * 10 - 5;
			int tempy = 3 + 4 * end.y - 1;
			gotoxy(tempx, tempy);
			cout << " ";
			gotoxy(tempx, tempy - 1);
			cout << " ";
		}
		else if (line[0] == 2)
		{

			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * end.y + 1;
			gotoxy(tempx, tempy);
			cout << " ";
			gotoxy(tempx, tempy + 1);
			cout << " ";

		}
		else if (line[0] == 3)
		{
			int tempx = end.x * 10 + 5;
			int tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "     ";
			end.x++;
		}
		else
		{

			tempx = end.x * 10 + 1;
			tempy = 3 + 4 * end.y + 2;
			gotoxy(tempx, tempy);
			cout << "     ";
		}

	}
	


}

//dfs algorithm
bool dfs(int** Pikachu, Point start, Point end, int line[65], int n, bool draw)
{
	//base case: when start point and end point is the same
	if (start.x == end.x && start.y == end.y && checkLine(line, n))
	{
		//to draw line
		if (draw)
		{
			path(end, line, n);
			Sleep(500);
			deletePath(end, line, n);
		}
		return true;
	}

	//to save trace
	if (Pikachu[start.x][start.y] == 0)
	{
		Pikachu[start.x][start.y] = -1;
	}

	//to turn up, down, left, right
	for (int k = 0; k < 4; k++)
	{
		//to save  the directions value to array Line and plus 1 with n’data to update direction change values.
		if (k != 0)
		{
			n--;
		}
		line[n] = k;
		n++;

		if (!checkLine(line, n)) continue;
		if (n > 100)
		{
			return false;
		}

		//creat new point for going to next location by using variable k[]
		Point p1Temp;
		p1Temp.x = start.x + dx[k];
		p1Temp.y = start.y + dy[k];

		//recursion case:
		if (exist(p1Temp) && (Pikachu[p1Temp.x][p1Temp.y] == 0 || (p1Temp.x == end.x && p1Temp.y == end.y)))
		{
			if (dfs(Pikachu, p1Temp, end, line, n, draw))
			{

				return true;
			}
		}
	}

	////to unsave trace
	Pikachu[start.x][start.y] = 0;

	return false;

}

//count the number of one column
int cntCol(int** Pikachu, Point& p)
{
	int cnt = 0;
	for (int i = 1; i <= HEIGHT; i++)
	{
		if (Pikachu[p.x][i] != 0) cnt++;
	}
	return cnt;
}

//count the number of one row
int cntRow(int** Pikachu, Point& p)
{
	int cnt = 0;
	for (int i = 1; i <= WIDTH; i++)
	{
		if (Pikachu[i][p.y] != 0) cnt++;
	}
	return cnt;
}


void moveRight(int** Pikachu, Point& p)
{
	int temp = p.x;
	do
	{
		p.x++;
		if (p.x > WIDTH) p.x = 1;

		if (Pikachu[p.x][p.y] != 0)
		{
			break;
		}
		else
		{
			int cnt = cntCol(Pikachu, p);
			if (cnt == 0) continue;
			int tempy = p.y;
			while (Pikachu[p.x][p.y] == 0 && p.y > 1)
			{
				p.y--;
			}

			if (Pikachu[p.x][p.y] != 0)
			{
				break;
			}

			p.y = tempy;
			while (Pikachu[p.x][p.y] == 0 && p.y < HEIGHT)
			{
				p.y++;
			}
			if (Pikachu[p.x][p.y] != 0)
			{
				break;
			}
		}
	} while (true);
}
void moveDown(int** Pikachu, Point& p)
{
	int temp = p.y;
	do
	{
		p.y++;
		if (p.y > HEIGHT) p.y = 1;
	} while (Pikachu[p.x][p.y] == 0 && p.y != temp);

	if (p.y == temp)
	{
		moveRight(Pikachu, p);
	}
}
void moveLeft(int** Pikachu, Point& p)
{
	int temp = p.x;
	do
	{
		p.x--;
		if (p.x < 1) p.x = WIDTH;
	} while (Pikachu[p.x][p.y] == 0 && p.x != temp);

	if (p.x == temp)
	{

		moveUp(Pikachu, p);
	}
}
void moveUp(int** Pikachu, Point& p)
{
	int temp = p.y;
	do
	{
		p.y--;
		if (p.y < 1) p.y = HEIGHT;

		if (Pikachu[p.x][p.y] != 0)
		{
			break;
		}
		else
		{
			int cnt = cntRow(Pikachu, p);
			if (cnt == 0) continue;
			int tempx = p.x;
			while (Pikachu[p.x][p.y] == 0 && p.x > 1)
			{
				p.x--;
			}

			if (Pikachu[p.x][p.y] != 0)
			{
				break;
			}

			p.x = tempx;
			while (Pikachu[p.x][p.y] == 0 && p.x < WIDTH)
			{
				p.x++;
			}
			if (Pikachu[p.x][p.y] != 0)
			{
				break;
			}
		}
	} while (true);
}

//to control moving
void move(int** Pikachu, Point& p, Point& t, bool& stop)
{
	bool flag = false;
	char ch;
	while (true)
	{
		ch = _getch();

		if (ch == ENTER)
		{
			playSoundChoose();
			if (!flag)
			{
				t = p;
				flag = true;
				Box(Pikachu[t.x][t.y], t.x, t.y, BLUE, BLACK);
			}
			else
			{
				Box(Pikachu[p.x][p.y], p.x, p.y, BLUE, BLACK);
				return;
			}
		}
		else if (ch == SPACE)
		{
			moveSuggest(Pikachu, p);
		}
		else if (ch == ESC)
		{
			stop = true;
			return;
		}
		else
		{
			ch = _getch();

			Point temp = p;
			if (ch == RIGHT)
			{
				moveRight(Pikachu, p);

			}
			else if (ch == LEFT)
			{
				moveLeft(Pikachu, p);
			}
			else if (ch == UP)
			{
				moveUp(Pikachu, p);

			}
			else if (ch == DOWN)
			{
				moveDown(Pikachu, p);
			}
			//redraw old location
			Box(Pikachu[temp.x][temp.y], temp.x, temp.y, BLACK, Pikachu[temp.x][temp.y] % 4 + 2);
			//draw new location
			Box(Pikachu[p.x][p.y], p.x, p.y, WHITE, BLACK);
			if (flag)
			{
				Box(Pikachu[t.x][t.y], t.x, t.y, BLUE, BLACK);
			}
		}
	}

}

//find vaild path for helping player
bool moveSuggest(int** Pikachu, Point& p)
{
	Point p1, p2;

	//travel into valid date
	for (p1.x = 1; p1.x <= WIDTH; p1.x++)
	{
		for (p1.y = 1; p1.y <= HEIGHT; p1.y++)
		{
			if (Pikachu[p1.x][p1.y] == 0) continue;

			//find valid data have same value
			for (p2.x = 1; p2.x <= WIDTH; p2.x++)
			{
				for (p2.y = 1; p2.y <= HEIGHT; p2.y++)
				{
					if (Pikachu[p1.x][p1.y] != Pikachu[p2.x][p2.y]) continue;
					if (p1.x == p2.x && p1.y == p2.y) continue;
					int line[65];

					//use dfs to find valid path, if not retun false
					int** temp = Double(Pikachu);
					if (dfs(temp, p1, p2, line, 0, false))
					{
						Box(Pikachu[p1.x][p1.y], p1.x, p1.y, GREEN, BLACK);
						Box(Pikachu[p2.x][p2.y], p2.x, p2.y, GREEN, BLACK);
						Sleep(1000);

						Box(Pikachu[p1.x][p1.y], p1.x, p1.y, BLACK, Pikachu[p1.x][p1.y] % 4 + 2);
						Box(Pikachu[p2.x][p2.y], p2.x, p2.y, BLACK, Pikachu[p2.x][p2.y] % 4 + 2);

						Box(Pikachu[p.x][p.y], p.x, p.y, WHITE, BLACK);
						deleteAll(temp);
						return true;
					}
					deleteAll(temp);

				}
			}

		}
	}
	return false;
}

//work as the same moveSuggest but it using to check next valid pair through programing
bool moveCheck(int** Pikachu, Point& p)
{
	Point p1, p2;
	for (p1.x = 1; p1.x <= WIDTH; p1.x++)
	{
		for (p1.y = 1; p1.y <= HEIGHT; p1.y++)
		{
			if (Pikachu[p1.x][p1.y] == 0) continue;

			for (p2.x = 1; p2.x <= WIDTH; p2.x++)
			{
				for (p2.y = 1; p2.y <= HEIGHT; p2.y++)
				{
					if (Pikachu[p1.x][p1.y] != Pikachu[p2.x][p2.y]) continue;
					if (p1.x == p2.x && p1.y == p2.y) continue;
					int line[65];

					int** temp = Double(Pikachu);
					if (dfs(temp, p1, p2, line, 0, false))
					{

						deleteAll(temp);
						return true;
					}
					deleteAll(temp);

				}
			}

		}
	}
	return false;
}
