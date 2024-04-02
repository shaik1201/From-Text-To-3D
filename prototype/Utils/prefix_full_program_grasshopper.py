import Grasshopper as gh
import System.Drawing as sd
comp = ghenv.Component
ghdoc = comp.OnPingDocument()

def AddParam(name, IO):
    assert IO in ('Output', 'Input')
    params = [param.NickName for param in getattr(ghenv.Component.Params, IO)]
    if name not in params:
        param = gh.Kernel.Parameters.Param_GenericObject()
        param.NickName = name
        param.Name = name
        param.Description = name
        param.Optional = True
        index = getattr(ghenv.Component.Params, IO).Count
        registers = dict(Input='RegisterInputParam', Output='RegisterOutputParam')
        getattr(ghenv.Component.Params, registers[IO])(param, index)
        
        return param
    return None

def AddSlider(min, max, value, target, index):
    slider = gh.Kernel.Special.GH_NumberSlider()
    slider.Slider.Maximum = max
    slider.Slider.Minimum = min
    slider.Slider.Value = value
    
    # calculate decimal point:
    decimal_places = 0
    split_val_by_point = str(value).split(".")
    if(len(split_val_by_point) > 1): 
        decimal_places = len(split_val_by_point[1])
            
    slider.Slider.DecimalPlaces = decimal_places
    ghdoc.AddObject(slider, False, ghdoc.ObjectCount + 1)
    
    # set the slider location
    thisBounds = ghenv.Component.Attributes.Bounds
    slider.Attributes.Pivot = sd.PointF(
        thisBounds.X-thisBounds.Width-200, thisBounds.Y + 20 + (25*index))
    target.AddSource(slider)

def RemoveExtraInputs(input_list):
    try:
        input_names = [input_.name for input_ in input_list] + ['code']
        extra_params = [param for param in getattr(ghenv.Component.Params, 'Input') if(param.NickName not in input_names)]
    
        for param in extra_params:
            print(param)
            if(param):
                print(param.NickName)
                for source in param.Sources:
                    ghdoc.RemoveObject(source,False)
                ghenv.Component.Params.UnregisterInputParameter(param)
        return len(extra_params)>0
    except Exception as error:
         print(error)
         return False

def expireThis(doc):
    comp.ExpireSolution(False)

class InputSlider():
    def __init__(self, name, value, min, max):
        self.name = name
        self.value = value
        self.min = min
        self.max = max

def create_params(input_list):
    deleted = RemoveExtraInputs(input_list)
    for i, input_ in enumerate(input_list):
        param = AddParam(input_.name, 'Input')
        if(param):
            AddSlider(input_.min, input_.max, input_.value, param, i)
    ghenv.Component.Params.OnParametersChanged()
    if(deleted):
        ghdoc.ScheduleSolution(1000,expireThis)