module CoinRefractor (
input  wire  [1:0]      Diameter,
input  wire  [1:0]      Weight,
output reg 	   Pound, // جنيه
output reg     Piaster, // نص جنيه
output reg     Nickel // ربع جنيه
);
reg [1:0] Specifications;

// 00 pound --- 01 Piaster ---- 10  Nickel -- 11 Invalid coin entered



always@(Diameter,Weight)
begin
	if(Diameter == 2'b11 && Weight == 2'b11)
        begin
            Specifications <= 2'b00; // Pound
        end
    else if(Diameter == 2'b10 && Weight == 2'b10 )
        begin
            Specifications <= 2'b01; // Piaster
        end
    else if(Diameter == 2'b01 && Weight == 2'b01)
        begin
            Specifications <= 2'b10;
        end
    else
        begin
        Specifications <= 2'b11;
        end

    case(Specifications)
2'b00 : begin
                Pound = 1'b1;
                Piaster = 1'b0;
                Nickel = 1'b0;
end

2'b01 : begin
                Pound = 1'b0;
                Piaster = 1'b1;
                Nickel = 1'b0;
end

2'b10 : begin
                Pound = 1'b0;
                Piaster = 1'b0;
                Nickel = 1'b1;
end

default : begin
                Pound = 1'b0;
                Piaster = 1'b0;
                Nickel = 1'b0;
end
    endcase

end
endmodule