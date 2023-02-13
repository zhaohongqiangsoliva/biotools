using DataFrames
using CSV
using ArgParse
function parse_commandline()
    s = ArgParseSettings()
    @add_arg_table s begin
        "-i" ,"--input"
            help = "an option with an argument"
        "-d" ,"--sep"
            help = "an option with an argument"
            default = ","

        "--comment", "-c"
            help = "another option with an argument"

        "--select"
            help = "an option without argument, i.e. a flag"
             default=nothing
        "--drop"
            help = "a positional argument"
            default = nothing
    end
    return parse_args(s)
end



function main()
    parsed_args = parse_commandline()
    print(typeof(parsed_args["select"]))
    if parsed_args["input"] != "any"

    		input_file=stdin
	else
		input_file=parsed_args["input"]
	end
    data = CSV.File(input_file,select=parsed_args["select"],drop=parsed_args["drop"],delim=parsed_args["sep"]) |> DataFrame
     print(data)

end

main()
