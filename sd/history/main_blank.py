import gc

while True:
	gc.collect()
	print(str(gc.mem_free()/1000)+"kb")
