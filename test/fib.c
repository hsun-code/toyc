int a = 2;
int *p;

int fib(int num)
{
	if (num == 1) {
		return 1;
	} else {
		if (num == 2) {
			return 1;
		} else {
			return fib(num - 1) + fib(num - 2);
		}
	}
}
