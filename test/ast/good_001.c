int a = 2;
int b;
int *p;
int *q = &b;
int arr[10];

int foo()
{
	;
}

int bar(int a, int *b)
{
	return a + *b;
}

int fib(int num)
{
	if (num == 1) {
		return 1;
	} else {
		if (num == 2) {
			return fib(bar(num, 1));
		} else {
			return fib(num - 1) + fib(num - 2);
		}
	}
}

int test(int num)
{
	int a =2;
	int b;
	int *p;
	int *q = &b;
	int arr[10];
	
	arr[1] = 2;
	arr[b] = a;
	a = -b;
	a = -10;
	a = b = c;
	a = a + b - c;
	a = a - b + c;
	a = b / c * 2;
	a = a + b * c / 2 == -20;

	while(1) {
		;
	}

	for(a = 2; a + b; c)
	{
		while(a == 2) {
			;
		}
	}

	return -10;
}
