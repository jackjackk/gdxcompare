' Declare Option Constants
Const BIF_NONEWFOLDER = &H0200
Const BIF_RETURNONLYFSDIRS = &H1
 
Function Browse4Folder(strPrompt, intOptions, strRoot)
    Dim objFolder, objFolderItem, objShell
    Set objShell = CreateObject("Shell.Application")
    Set objFolder = objShell.BrowseForFolder(0, strPrompt, intOptions, strRoot) 
    If (objFolder Is Nothing) Then
        Browse4Folder = ""
    Else
        Set objFolderItem = objFolder.Self
        Browse4Folder = objFolderItem.Path      
        Set objFolderItem = Nothing
        Set objFolder = Nothing
    End If  
    Set objShell = Nothing
End Function
 
strPrompt = "Please select the GAMS main folder (e.g. C:\GAMS\win64\24.5)."
intOptions = BIF_RETURNONLYFSDIRS + BIF_NONEWFOLDER
 
' Return the path, e.g. C:\
strFolderPath = Browse4Folder(strPrompt, intOptions, "C:\GAMS")

Set wshShell = CreateObject( "WScript.Shell" )
Set wshUserEnv = wshShell.Environment( "USER" )
' Set GAMSDIR
wshUserEnv( "GAMSDIR" ) = strFolderpath
' Set PYTHONPATH
If InStr(wshUserEnv( "PYTHONPATH" ), strFolderpath) = 0 Then
    wshUserEnv( "PYTHONPATH" ) = strFolderpath & "\apifiles\Python\api;" & wshUserEnv( "PYTHONPATH" )
    WScript.Echo "PYTHONPATH updated!"
Else
    WScript.Echo "PYTHONPATH was already set up!"
End If

Set fso = CreateObject("Scripting.FileSystemObject")
strFolderpath = fso.GetAbsolutePathName(".")
If InStr(wshUserEnv( "PATH" ), strFolderpath) = 0 Then
    wshUserEnv( "PATH" ) = strFolderpath & ";" & wshUserEnv( "PATH" )
    WScript.Echo "PATH updated!"
Else
    WScript.Echo "PATH was already set up!"
End If
