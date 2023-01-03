module Test1 (
input  wire        HasAccess,
input  reg [3:0]   Input_Pin,
output reg [3:0]   message,
output reg 	   Welcome
);

reg [3:0] pin;


initial begin
	pin = 4'b1111;
end

always@(HasAccess)
begin
	case(HasAccess)
1'b1:
		begin
		message = 4'b1111;
		end
1'b0:
		begin
		message = 4'b0000;
		end
default: begin
			message=4'b0000;
		end
endcase
	if(message == 4'b1111 && Input_Pin == pin)
		begin
		Welcome <= 1'b1;
		end
	else
		begin
		Welcome <= 1'b0;
		end
end
endmodule