module Fingerprint_Attendance_System (
input  wire        OnTime,
input  wire        attendFlag,
input  reg [2:0]  Fingerprint,

output reg 	   AttendanceAccepted
//output reg     AlreadyAttended 
);
reg [2:0] employee1Print,employee2Print,employee3Print;
//reg attendFlag;
initial begin
	employee1Print=3'b001;
    employee2Print=3'b010;
    employee3Print=3'b011;
   // attendFlag=1'b0;

end
/* case(HasAccess)
1'b1:
        begin
        message = 4'b1111;
        end*/
always@(Fingerprint)
begin
	if(OnTime && attendFlag==1'b0 )
		begin
		case(Fingerprint)
        3'b001:
            begin
            AttendanceAccepted=1'b1;
          //  attendFlag=1'b1;
            end
        3'b010:
            begin
            AttendanceAccepted=1'b1;
           // attendFlag=1'b1;
            end
        3'b011:
            begin
            AttendanceAccepted=1'b1;
            //attendFlag=1'b1;
            end
        default:  
            begin
            AttendanceAccepted=1'b0;
          //  attendFlag=1'b1;
            end  
        endcase 
    end


    else
		begin
		AttendanceAccepted<=1'b0;
		end
	
end
// AlreadyAttended <= attendFlag & AttendanceAccepted;
endmodule