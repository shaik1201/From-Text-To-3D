comp = ghenv.Component
ghdoc = comp.OnPingDocument()

def clear_params():
    while len(comp.Params.Input) > 1: #do not delete the "code" param
        print(comp.Params.Input[len(ghenv.Component.Params.Input) - 1].NickName)
        if(comp.Params.Input[len(ghenv.Component.Params.Input) - 1]):
            if len(comp.Params.Input[len(ghenv.Component.Params.Input) - 1].Sources) > 0:
                ghdoc.RemoveObject(comp.Params.Input[len(ghenv.Component.Params.Input) - 1].Sources[0],False)
        comp.Params.UnregisterInputParameter(ghenv.Component.Params.Input[len(ghenv.Component.Params.Input) - 1])
        comp.Params.OnParametersChanged()
    

clear_params()