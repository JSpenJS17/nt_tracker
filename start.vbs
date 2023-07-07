Set WshShell = CreateObject("WScript.Shell")

file = "start_debug.bat"
dim fso, fullPathToFile
set fso = CreateObject("Scripting.FileSystemObject")
fullPathToFile = fso.GetAbsolutePathName(file)

WshShell.Run chr(34) & fullPathToFile & Chr(34), 0
Set WshShell = Nothing
