# put string in a array to a whole string
def strArray_to_str(arr, separator=','):
	length = len(arr)
	if length == 0:
		return ''
	
	res = arr[0]
	for i in range(1, length):
		res = res + separator + arr[i]
	return res;

# tranfer unicode-formatted string to uft-8
def unicode_to_utf8(uni_str):
	res = "";
	for i in uni_str:
		res = res + (i.encode('utf-8'))
	return res


