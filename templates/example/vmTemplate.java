public class [[VMType]] {
/*<SPLIT>*/		
/*<ITERATE>(property,'')*/
    private DataElement<[[property.type]]> [[property.name_lower]];
/*<SPLIT>*/
/*<ITERATE>(property,'')*/
    public DataElement<[[property.type]]> get[[property.name]]() {
        return [[property.name_lower]];
    }

    public void set[[property.name]](DataElement<[[property.type]]> [[property.name_lower]]) {
        this.[[property.name_lower]] = [[property.name_lower]];
    }
/*<SPLIT>*/
}
