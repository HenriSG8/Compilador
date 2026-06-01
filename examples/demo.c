int x;
bool ok;

x = read();
ok = x > 0;

while (ok) {
    print(x);
    x = x - 1;
    ok = x > 0;
}
